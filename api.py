import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pipeline.agent import ExtractionAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Loan Document Extraction API",
    description="Extract structured data from loan documents using AI",
    version="2.0.0"
)

agent = ExtractionAgent()


class ExtractionRequest(BaseModel):
    """Pydantic model - validates incoming requests."""
    document_id: str
    document_type: Optional[str] = None


class FieldResult(BaseModel):
    """Pydantic model - validates each extracted field."""
    value: Optional[str] = None
    confidence: float = 0.0
    method: str = ""


class ExtractionResponse(BaseModel):
    """Pydantic model - validates the API response."""
    document_id: str
    status: str
    loan_type: str
    valid: bool
    errors: list = []
    fields: dict = {}


@app.get("/health")
def health_check():
    """Check if API is running."""
    return {"status": "healthy", "version": "2.0.0"}


@app.post("/extract", response_model=ExtractionResponse)
def extract_document(request: ExtractionRequest):
    """Extract fields from a loan document."""
    try:
        logger.info(f"API request: extract {request.document_id}")
        state = agent.run(request.document_id)

        return ExtractionResponse(
            document_id=state["document_id"],
            status=state["status"],
            loan_type=state["final_result"].get("loan_type", "unknown"),
            valid=state["validation"]["valid"],
            errors=state["validation"]["errors"],
            fields=state["final_result"]
        )
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


