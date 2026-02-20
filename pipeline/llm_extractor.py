import logging
import json
from config.settings import Settings

logger = logging.getLogger(__name__)


class LLMExtractor:
    """Extracts loan fields using GPT-4 (Project 2 - AI approach)."""

    def __init__(self):
        self.settings = Settings()
        self.prompt_template = """You are a loan document extraction expert.
Extract the following fields from this loan document text.
Return ONLY valid JSON with these fields:

- borrower_name: Full name of the borrower
- loan_amount: Numeric amount (no $ or commas)
- interest_rate: Numeric rate (no % sign)
- loan_term: Number of months
- monthly_payment: Numeric amount (no $ or commas)
- loan_type: One of: personal_loan, auto_loan, commercial_loan, heloc, sba_loan

Document text:
{text}

JSON response:"""

    def extract(self, text):
        """Extract fields using LLM with fallback."""
        prompt = self.prompt_template.format(text=text)
        logger.info("Sending document to LLM for extraction...")

        try:
            # Try GPT-4 first (Azure OpenAI)
            result = self._call_gpt4(text)
            return result
        except Exception as e:
            logger.warning(f"GPT-4 failed: {e}, falling back to Claude")
            try:
                # Fallback to Claude (AWS Bedrock)
                result = self._call_claude(text)
                return result
            except Exception as e:
                logger.error(f"Both LLMs failed: {e}")
                return None

    def _call_gpt4(self, text):
        """Call GPT-4 via Azure OpenAI."""
        # In production: openai.chat.completions.create(...)
        # For now: mock response
        logger.info("Calling GPT-4 (mock)...")
        return self._mock_llm_response(text)

    def _call_claude(self, text):
        """Call Claude via AWS Bedrock."""
        # In production: bedrock.invoke_model(...)
        # For now: mock response
        logger.info("Calling Claude (mock)...")
        return self._mock_llm_response(text)


    def _mock_llm_response(self, text):
        """Simulate GPT-4 response for local testing."""
        # In production, this calls real GPT-4
        # GPT-4 understands meaning, not just patterns
        response = {
            "borrower_name": {"value": "John Smith", "confidence": 0.95, "method": "llm"},
            "loan_amount": {"value": "25000", "confidence": 0.97, "method": "llm"},
            "interest_rate": {"value": "5.99", "confidence": 0.96, "method": "llm"},
            "loan_term": {"value": "60", "confidence": 0.94, "method": "llm"},
            "monthly_payment": {"value": "483.15", "confidence": 0.93, "method": "llm"},
            "loan_type": "personal_loan"
        }
        logger.info("Using mock LLM response (no API key)")
        return response
