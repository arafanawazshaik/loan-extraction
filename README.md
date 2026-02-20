# Loan Document Extraction Pipeline

AI-powered pipeline that extracts structured data from loan documents using OCR, rule-based extraction, and LLM consensus scoring.

## Architecture
```
PDF Upload → FastAPI
               ↓
         AWS Textract (OCR)
               ↓
         Text Cleaner (preprocessing)
               ↓
         RAG (chunk + embed + retrieve)
               ↓
    ┌──────────┴──────────┐
    ↓                     ↓
Rule Engine (regex)   LLM Extractor (GPT-4 → Claude)
    ↓                     ↓
    └──────────┬──────────┘
               ↓
         Consensus Checker
               ↓
         Guardrails (hallucination check)
               ↓
         Validator (business rules)
               ↓
         Agent Decision (approve/review)
               ↓
         DynamoDB (store results)
```

## Features

- **Dual Extraction**: Rule-based regex + LLM extraction with consensus scoring
- **Multi-Model Fallback**: GPT-4 (Azure OpenAI) → Claude (AWS Bedrock) → Rule-based
- **RAG Pipeline**: Document chunking, embeddings, and vector retrieval
- **Guardrails**: Cross-checks LLM outputs against source to prevent hallucinations
- **Agentic Workflow**: LangGraph-style agent with intelligent decision making
- **REST API**: FastAPI with Pydantic validation and Swagger docs
- **Monitoring**: Pipeline step timing, token tracking, and cost estimation
- **Storage**: DynamoDB for audit trail and compliance
- **CI/CD**: GitHub Actions for automated testing and Docker builds

## Tech Stack

- **Language**: Python
- **API**: FastAPI, Pydantic, Uvicorn
- **AI/ML**: LangChain, LangGraph, OpenAI GPT-4, AWS Bedrock (Claude)
- **RAG**: SentenceTransformers, LangChain Text Splitters
- **OCR**: AWS Textract
- **Storage**: Amazon S3, DynamoDB
- **Infrastructure**: Docker, LocalStack, GitHub Actions
- **Monitoring**: Custom pipeline monitor (LangSmith-ready)

## Project Structure
```
loan-extraction/
├── api.py                      # FastAPI REST API
├── main.py                     # CLI entry point
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # LocalStack + services
├── requirements.txt            # Dependencies
├── .github/workflows/ci.yml    # CI/CD pipeline
├── config/
│   └── settings.py             # Dataclass configurations
└── pipeline/
    ├── textract_client.py      # AWS Textract OCR
    ├── mock_textract.py        # Local OCR mock
    ├── table_stitcher.py       # Multi-page table handling
    ├── text_cleaner.py         # OCR text preprocessing
    ├── classifier.py           # Document type classification
    ├── rule_engine.py          # Regex-based extraction
    ├── llm_extractor.py        # GPT-4/Claude extraction
    ├── rag_retriever.py        # RAG chunking and retrieval
    ├── consensus.py            # Rule vs LLM comparison
    ├── guardrails.py           # Hallucination detection
    ├── validator.py            # Business rule validation
    ├── dynamodb_store.py       # Result storage
    ├── monitoring.py           # Performance tracking
    └── agent.py                # Pipeline orchestrator
```

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI
python main.py

# Run API server
uvicorn api:app --reload

# API docs
open http://localhost:8000/docs
```

## API Endpoints
```
GET  /health    → Health check
POST /extract   → Extract fields from loan document
```

### Example Request
```json
POST /extract
{
    "document_id": "test_loan.pdf",
    "document_type": "personal_loan"
}
```

### Example Response
```json
{
    "document_id": "test_loan.pdf",
    "status": "approved",
    "loan_type": "personal_loan",
    "valid": true,
    "fields": {
        "borrower_name": {"value": "John Smith", "confidence": 0.95, "method": "consensus"},
        "loan_amount": {"value": "25000", "confidence": 0.97, "method": "llm_preferred"},
        "interest_rate": {"value": "5.99", "confidence": 0.96, "method": "consensus"},
        "loan_term": {"value": "60", "confidence": 0.94, "method": "consensus"},
        "monthly_payment": {"value": "483.15", "confidence": 0.93, "method": "consensus"}
    }
}
```

## Pipeline Flow

1. **OCR**: Textract extracts text from scanned documents
2. **Clean**: Remove OCR artifacts and normalize text
3. **RAG**: Chunk document, create embeddings, store vectors
4. **Extract**: Run both rule-based and LLM extraction
5. **Consensus**: Compare results, pick best answer per field
6. **Guardrails**: Verify values exist in source document
7. **Validate**: Apply business rules (amount limits, rate ranges)
8. **Decide**: Agent approves or flags for human review
9. **Store**: Save results to DynamoDB for audit
