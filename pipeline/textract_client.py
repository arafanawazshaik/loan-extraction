import os
import boto3
import logging
from config.settings import Settings
from pipeline.mock_textract import MockTextract

logger = logging.getLogger(__name__)


class TextractClient:
    """Client for AWS Textract."""

    def __init__(self):
        self.settings = Settings()
        if os.getenv("USE_MOCK", "true").lower() == "true":
            self.client = MockTextract()
            logger.info("Using MockTextract for local development")
        else:
            self.client = boto3.client('textract', region_name=self.settings.aws.region)
            logger.info("Using real AWS Textract")

    def process_document(self, document_id, s3_bucket=None, page_count=1):
        """Process a document from S3 using Textract."""
        if s3_bucket is None:
            s3_bucket = self.settings.aws.s3_bucket

        logger.info(f"Processing document: {document_id} from bucket: {s3_bucket}")

        if self.needs_chunking(page_count):
            chunks = self.chunk_pages(page_count)
            results = []
            for chunk in chunks:
                logger.info(f"Processing chunk: pages {chunk[0]} to {chunk[1]}")
                response = self.call_textract(document_id, s3_bucket)
                results.append(response)
            return results
        else:
            return self.call_textract(document_id, s3_bucket)

    def call_textract(self, document_id, s3_bucket):
        """Send document to Textract and get results."""
        try:
            response = self.client.analyze_document(
                Document={
                    'S3Object': {
                        'Bucket': s3_bucket,
                        'Name': document_id
                    }
                },
                FeatureTypes=['TABLES', 'FORMS']
            )
            logger.info(f"Textract returned {len(response['Blocks'])} blocks")
            return response
        except Exception as e:
            logger.error(f"Textract failed for {document_id}: {e}")
            raise

    def needs_chunking(self, page_count):
        """Check if document needs to be split into chunks."""
        max_pages = self.settings.textract.max_pages
        if page_count > max_pages:
            logger.info(f"Document has {page_count} pages, exceeds {max_pages}. Chunking needed.")
            return True
        logger.info(f"Document has {page_count} pages, no chunking needed.")
        return False

    def chunk_pages(self, total_pages):
        """Split page numbers into chunks."""
        chunk_size = self.settings.textract.chunk_size
        chunks = []
        for start in range(0, total_pages, chunk_size):
            end = min(start + chunk_size, total_pages)
            chunks.append((start + 1, end))
        logger.info(f"Split {total_pages} pages into {len(chunks)} chunks: {chunks}")
        return chunks