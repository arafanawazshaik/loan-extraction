import logging
from pipeline.classifier import DocumentClassifier
from pipeline.rule_engine import RuleEngine
from pipeline.validator import Validator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_pipeline(document_id):
    """Run the full extraction pipeline on a document."""
    logger.info(f"=== Starting pipeline for {document_id} ===")

    # Step 1: OCR - Skip for now (will use LocalStack later)
    logger.info("Step 1: OCR skipped (no AWS credentials yet)")
    sample_text = "Borrower: John Smith Loan Amount: $25,000 Interest Rate: 5.99% Term: 60 months"

    # Step 2: Classify
    logger.info("Step 2: Classifying document...")
    classifier = DocumentClassifier()
    classification = classifier.classify(sample_text)
    loan_type = classification["loan_type"]

    # Step 3: Extract
    logger.info("Step 3: Extracting fields...")
    extractor = RuleEngine()
    extracted = extractor.extract(sample_text, loan_type)

    # Step 4: Validate
    logger.info("Step 4: Validating...")
    validator = Validator()
    validation = validator.validate(extracted)

    # Step 5: Results
    logger.info(f"=== Pipeline complete for {document_id} ===")
    return {
        "document_id": document_id,
        "loan_type": loan_type,
        "extracted_fields": extracted,
        "validation": validation
    }


if __name__ == "__main__":
    result = run_pipeline("loan-doc-123.pdf")
    print("\n=== FINAL RESULT ===")
    print(f"Document: {result['document_id']}")
    print(f"Loan Type: {result['loan_type']}")
    print(f"Valid: {result['validation']['valid']}")
    for field, data in result['extracted_fields'].items():
        if isinstance(data, dict):
            print(f"  {field}: {data['value']}")



