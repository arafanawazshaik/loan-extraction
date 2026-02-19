import logging
from config.settings import Settings

logger = logging.getLogger(__name__)


class Validator:
    """Validates extracted loan fields against business rules."""

    def __init__(self):
        self.settings = Settings()

    def validate(self, extracted_data):
        """Validate extracted fields against business rules."""
        errors = []

        amount = extracted_data.get("loan_amount", {}).get("value")
        if amount:
            amount_num = float(amount.replace(",", ""))
            if amount_num > self.settings.validation.max_loan_amount:
                errors.append(f"Loan amount ${amount_num} exceeds max ${self.settings.validation.max_loan_amount}")
                logger.error(f"Validation failed: loan amount too high")

        rate = extracted_data.get("interest_rate", {}).get("value")
        if rate:
            rate_num = float(rate)
            if rate_num > self.settings.validation.max_interest_rate:
                errors.append(f"Interest rate {rate_num}% exceeds max {self.settings.validation.max_interest_rate}%")
                logger.error(f"Validation failed: interest rate too high")

        term = extracted_data.get("loan_term", {}).get("value")
        if term:
            term_num = int(term)
            if term_num > self.settings.validation.max_loan_term_months:
                errors.append(f"Loan term {term_num} months exceeds max {self.settings.validation.max_loan_term_months}")
                logger.error(f"Validation failed: loan term too long")

        if errors:
            logger.warning(f"Validation found {len(errors)} errors")
            return {"valid": False, "errors": errors}

        logger.info("Validation passed")
        return {"valid": True, "errors": []}
