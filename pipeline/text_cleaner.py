import re
import logging

logger = logging.getLogger(__name__)


class TextCleaner:
    """Cleans raw Textract output before extraction."""

    def clean(self, raw_text):
        """Clean messy OCR text."""
        text = raw_text

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Fix common OCR errors
        text = text.replace('|', 'l')       # pipe mistaken for L
        text = text.replace('0rrow', 'orrow')  # zero mistaken for O in "Borrower"
        text = text.replace('$S', '$5')      # S mistaken for 5

        # Remove garbage characters
        text = re.sub(r'[^\x20-\x7E\n]', '', text)

        # Normalize common patterns
        text = re.sub(r'(\d),(\d{3})', r'\1,\2', text)  # fix broken numbers like 25, 000

        text = text.strip()
        logger.info(f"Cleaned text: {len(raw_text)} chars → {len(text)} chars")
        return text