
import os
from dataclasses import dataclass , field
@dataclass
class AWSConfig:
    region: str = os.getenv("AWS_REGION", "us-east-1")  
    s3_bucket: str = os.getenv("S3_DOCUMENT_BUCKET", "loan-documents-dev")
    sqs_queue_url: str = os.getenv("SQS_QUEUE_URL","")
    dynamodb_table: str = os.getenv("DYNAMODB_TABLE", "loan-extractions-dev")
@dataclass
class TextractConfig:
    max_pages : int = int(os.getenv("TEXTRACT_MAX_PAGES", "40"))
    chunk_size : int = int(os.getenv("TEXTRACT_CHUNK_SIZE", "35"))
    timeout_seconds :int = int(os.getenv("TEXTRACT_TIMEOUT", "300"))
@dataclass
class ClassifierConfig:
    model_path :str = os.getenv("CLASSIFIER_MODEL_PATH", "models/classifier.joblib")
    confidence_threshold : float = float(os.getenv("CLASSIFIER_CONFIDENCE", "0.85"))
@dataclass
class ExtractionConfig:
    hitl_confidence_threshold : float = float(os.getenv("HITL_THRESHOLD", "0.80"))
    max_retries : int = int(os.getenv("EXTRACTION_MAX_RETRIES", "3"))
    supported_loan_types : str = os.getenv("SUPPORTED_LOAN_TYPES","personal_loan,auto_loan,commercial_loan,heloc,sba_loan")
@dataclass
class ValidationConfig:
    max_loan_amount : float = float(os.getenv("MAX_LOAN_AMOUNT", "50000000.0"))
    max_interest_rate : float = float(os.getenv("MAX_INTEREST_RATE", "35.0"))  
    max_loan_term_months : int = int(os.getenv("MAX_LOAN_TERM_MONTHS", "480"))
@dataclass
class MonitoringConfig:
    log_level : str = os.getenv("LOG_LEVEL", "INFO")     
    enable_metrics: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"
@dataclass
class Settings:
    aws: AWSConfig = field(default_factory=AWSConfig)
    textract: TextractConfig = field(default_factory=TextractConfig)
    classifier: ClassifierConfig = field(default_factory=ClassifierConfig)
    extraction: ExtractionConfig = field(default_factory=ExtractionConfig)
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    environment: str = os.getenv("ENVIRONMENT", "development")
settings = Settings()

