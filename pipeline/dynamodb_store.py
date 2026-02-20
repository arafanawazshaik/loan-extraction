import logging
import json
import os
import boto3
from datetime import datetime
from config.settings import settings

logger = logging.getLogger(__name__)


class DynamoDBStore:
    """Stores extraction results in DynamoDB."""

    def __init__(self):
        localstack_endpoint = os.environ.get('LOCALSTACK_ENDPOINT', 'http://localhost:4566')
        use_localstack = os.environ.get('USE_LOCALSTACK', 'true').lower() == 'true'

        if use_localstack:
            self.dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=localstack_endpoint,
                region_name=settings.aws.region,
                aws_access_key_id='test',
                aws_secret_access_key='test'
            )
        else:
            self.dynamodb = boto3.resource('dynamodb', region_name=settings.aws.region)

        self.table_name = settings.aws.dynamodb_table
        self._ensure_table()
        logger.info("DynamoDB store initialized")

    def _ensure_table(self):
        """Create table if it doesn't exist."""
        try:
            self.table = self.dynamodb.Table(self.table_name)
            self.table.load()
            logger.info(f"Table '{self.table_name}' exists")
        except Exception:
            try:
                self.table = self.dynamodb.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {'AttributeName': 'document_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'processed_at', 'KeyType': 'RANGE'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'document_id', 'AttributeType': 'S'},
                        {'AttributeName': 'processed_at', 'AttributeType': 'S'}
                    ],
                    BillingMode='PAY_PER_REQUEST'
                )
                self.table.wait_until_exists()
                logger.info(f"Created table '{self.table_name}'")
            except Exception as e:
                logger.warning(f"Could not create table: {e}")
                self.table = None


    def store_result(self, state):
        """Save extraction result to DynamoDB."""
        if self.table is None:
            logger.warning("No DynamoDB table available, skipping store")
            return None

        item = {
            'document_id': state['document_id'],
            'processed_at': datetime.now().isoformat(),
            'status': state['status'],
            'valid': state['validation']['valid'],
            'fields': json.dumps(state['final_result']),
            'guardrails_passed': state.get('guardrails', {}).get('passed', False)
        }

        try:
            self.table.put_item(Item=item)
            logger.info(f"Stored result for {state['document_id']} in DynamoDB")
            return item
        except Exception as e:
            logger.error(f"Failed to store in DynamoDB: {e}")
            return None
