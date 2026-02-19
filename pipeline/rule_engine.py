import re
import logging
from config.settings import Settings

logger = logging.getLogger(__name__)


class RuleEngine:
    """Extracts loan fields using pattern-matching rules (Project 1)."""

    def __init__(self):
        self.settings = Settings()
        self.patterns = {
            "borrower_name": r"(?:borrower|applicant|name)\s*[:\-]\s*([A-Z][a-z]+ [A-Z][a-z]+)",
            "loan_amount": r"(?:loan amount|principal|amount)\s*[:\-]\s*\$?([\d,]+\.?\d*)",
            "interest_rate": r"(?:interest rate|rate|apr)\s*[:\-]\s*([\d.]+)\s*%",
            "loan_term": r"(?:term|duration|period)\s*[:\-]\s*(\d+)\s*(?:months|month)",
            "monthly_payment": r"(?:monthly payment|payment)\s*[:\-]\s*\$?([\d,]+\.?\d*)"
        }

    def extract(self, text, loan_type):
        """Extract fields from document text using regex patterns."""
        results = {}

        for field_name, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                results[field_name] = {
                    "value": match.group(1),
                    "confidence": 0.85,
                    "method": "rule_based"
                }
                logger.info(f"Found {field_name}: {match.group(1)}")
            else:
                results[field_name] = {
                    "value": None,
                    "confidence": 0.0,
                    "method": "rule_based"
                }
                logger.warning(f"Could not find {field_name}")

        results["loan_type"] = loan_type
        return results