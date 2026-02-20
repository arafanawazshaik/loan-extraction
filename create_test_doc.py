import boto3

# Create a text version of a loan document
loan_text = """
PERSONAL LOAN AGREEMENT

Borrower: John Smith
Loan Amount: $25,000
Interest Rate: 5.99%
Term: 60 months
Monthly Payment: $483.15

This agreement is between the borrower and First National Bank.
The borrower agrees to repay the principal amount plus interest
over the specified term period.
"""

# Save as text file
with open("test_loan.txt", "w") as f:
    f.write(loan_text)
print("Text file created: test_loan.txt")

# Upload to fake S3
s3 = boto3.client('s3', endpoint_url='http://localhost:4566',
    aws_access_key_id='test', aws_secret_access_key='test', region_name='us-east-1')
s3.upload_file("test_loan.txt", "loan-documents-dev", "test_loan.txt")
print("Uploaded to fake S3: loan-documents-dev/test_loan.txt")

