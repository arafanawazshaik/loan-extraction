import logging

logger = logging.getLogger(__name__)


class MockTextract:
    """Simulates AWS Textract for local testing."""

    def analyze_document(self, Document, FeatureTypes):
        """Return fake Textract response like real AWS would."""
        logger.info("MockTextract: Analyzing document...")

        # This is what real Textract returns - a list of blocks
        response = {
            'Blocks': [
                {
                    'BlockType': 'PAGE',
                    'Text': '',
                    'Id': 'page-1'
                },
                {
                    'BlockType': 'LINE',
                    'Text': 'PERSONAL LOAN AGREEMENT',
                    'Id': 'line-1'
                },
                {
                    'BlockType': 'LINE',
                    'Text': 'Borrower: John Smith',
                    'Id': 'line-2'
                },
                {
                    'BlockType': 'LINE',
                    'Text': 'Loan Amount: $25,000',
                    'Id': 'line-3'
                },
                {
                    'BlockType': 'LINE',
                    'Text': 'Interest Rate: 5.99%',
                    'Id': 'line-4'
                },
                {
                    'BlockType': 'LINE',
                    'Text': 'Term: 60 months',
                    'Id': 'line-5'
                },
                {
                    'BlockType': 'LINE',
                    'Text': 'Monthly Payment: $483.15',
                    'Id': 'line-6'
                }
            ]
        }

        logger.info(f"MockTextract: Returned {len(response['Blocks'])} blocks")
        return response
