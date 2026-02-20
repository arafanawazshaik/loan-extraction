import logging
import re

logger = logging.getLogger(__name__)


class Guardrails:
    """Validates LLM outputs against source text to prevent hallucinations."""

    def check(self, extracted_data, source_text):
        """Verify extracted values actually exist in the source document."""
        issues = []
        source_lower = source_text.lower()

        fields = ["borrower_name", "loan_amount", "interest_rate", "loan_term", "monthly_payment"]

        for field in fields:
            data = extracted_data.get(field, {})
            if not isinstance(data, dict):
                continue

            value = data.get("value")
            if value is None:
                continue

            # Check if the value exists in the source text
            if not self._value_in_source(value, source_lower):
                issues.append({
                    "field": field,
                    "value": value,
                    "issue": "hallucination",
                    "message": f"{field} value '{value}' not found in source document"
                })
                logger.warning(f"HALLUCINATION DETECTED: {field}='{value}' not in source")
            else:
                logger.info(f"Verified: {field}='{value}' found in source")

        if issues:
            logger.warning(f"Guardrails found {len(issues)} potential hallucinations")
        else:
            logger.info("Guardrails passed: all values verified in source")

        return {"passed": len(issues) == 0, "issues": issues}

    def _value_in_source(self, value, source_text):
        """Check if a value appears in the source text."""
        value_lower = str(value).lower()

        # Direct match
        if value_lower in source_text:
            return True

        # Number match (handle formatting: "25000" vs "25,000" vs "$25,000")
        numbers = re.findall(r'[\d,]+\.?\d*', value_lower)
        for num in numbers:
            clean_num = num.replace(",", "")
            if clean_num in source_text.replace(",", ""):
                return True

        # Name parts match (handle "John Smith" vs "john smith")
        parts = value_lower.split()
        if len(parts) > 1 and all(part in source_text for part in parts):
            return True

        return False
