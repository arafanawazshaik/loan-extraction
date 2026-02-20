import logging
from pipeline.agent import ExtractionAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_pipeline(document_id):
    """Run the agentic extraction pipeline."""
    agent = ExtractionAgent()
    state = agent.run(document_id)
    return state


if __name__ == "__main__":
    result = run_pipeline("test_loan.pdf")

    print("\n=== FINAL RESULT ===")
    print(f"Document: {result['document_id']}")
    print(f"Status: {result['status']}")
    print(f"Valid: {result['validation']['valid']}")
    for field, data in result['final_result'].items():
        if isinstance(data, dict):
            print(f"  {field}: {data['value']} (confidence: {data['confidence']:.2f}, method: {data['method']})")


