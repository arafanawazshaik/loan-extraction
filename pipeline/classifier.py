import logging
from config.settings import Settings

logger = logging.getLogger(__name__)


class DocumentClassifier:
    """Classifies loan documents into types (personal, auto, commercial, etc.)."""

    def __init__(self):
        self.settings = Settings()
        self.keyword_map = {
            "personal_loan": ["borrower", "personal", "unsecured", "apr", "monthly payment"],
            "auto_loan": ["vehicle", "vin", "dealer", "mileage", "auto"],
            "commercial_loan": ["commercial", "business", "dscr", "ltv", "collateral"],
            "heloc": ["credit limit", "draw period", "heloc", "home equity", "cltv"],
            "sba_loan": ["sba", "guarantee", "7(a)", "small business", "proceeds"]
        }

    def classify(self, text):
        """Classify document text into a loan type."""
        text_lower = text.lower()
        scores = {}

        for loan_type, keywords in self.keyword_map.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            scores[loan_type] = score / len(keywords)

        best_type = max(scores, key=scores.get)
        confidence = scores[best_type]

        logger.info(f"Classification: {best_type} (confidence: {confidence:.2f})")

        if confidence >= self.settings.classifier.confidence_threshold:
            return {"loan_type": best_type, "confidence": confidence, "method": "keyword"}
        else:
            logger.warning(f"Low confidence {confidence:.2f}, below threshold")
            return {"loan_type": best_type, "confidence": confidence, "method": "low_confidence"}