# Loan Document Extraction Pipeline

Automated system for extracting structured data from loan documents using AWS services and rule-based processing.

## Architecture

```
PDF → Textract (OCR) → Classifier → Rule Engine → Validator → Results
```

## Project Structure

```
loan-extraction/
├── config/
│   └── settings.py              # Pipeline configuration (7 config classes)
├── pipeline/
│   ├── textract_client.py       # AWS Textract OCR client with chunking
│   ├── mock_textract.py         # Mock Textract for local development
│   ├── table_stitcher.py        # Merges tables split across pages (LOAN-BUG-001)
│   ├── classifier.py            # Keyword-based document classification
│   ├── rule_engine.py           # Regex pattern extraction for loan fields
│   └── validator.py             # Business rule validation
├── main.py                      # Pipeline orchestrator
├── create_test_doc.py           # Test document generator
├── docker-compose.yml           # LocalStack setup
└── requirements.txt             # Python dependencies
```

## Supported Loan Types

- Personal Loan
- Auto Loan
- Commercial Loan
- HELOC (Home Equity Line of Credit)
- SBA Loan

## Extracted Fields

- Borrower Name
- Loan Amount
- Interest Rate
- Loan Term
- Monthly Payment

## Setup

### Prerequisites
- Python 3.11+
- Docker Desktop
- Git

### Installation
```bash
git clone https://github.com/arafanawazshaik/loan-extraction.git
cd loan-extraction
pip install -r requirements.txt
```

### Run LocalStack
```bash
docker compose up -d
```

### Create Test Document
```bash
python create_test_doc.py
```

### Run Pipeline
```bash
python main.py
```

## Sample Output

```
Document: test_loan.pdf
Loan Type: personal_loan
Valid: True
  borrower_name: John Smith
  loan_amount: 25,000
  interest_rate: 5.99
  loan_term: 60
  monthly_payment: 483.15
```

## Tech Stack

- **Python** - Core language
- **AWS Textract** - OCR document processing
- **AWS S3** - Document storage
- **Docker + LocalStack** - Local AWS development
- **Git/GitHub** - Version control with feature branch workflow

## Coming Next (Project 2)

- Agentic AI extraction using GPT-4 and LangGraph
- 94% accuracy vs 78% rule-based
- Multi-model consensus with Claude verification
