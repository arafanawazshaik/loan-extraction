import logging
from py_compile import main
from pipeline.textract_client import TextractClient
from pipeline.text_cleaner import TextCleaner
from pipeline.classifier import DocumentClassifier
from pipeline.rule_engine import RuleEngine
from pipeline.llm_extractor import LLMExtractor
from pipeline.consensus import ConsensusChecker
from pipeline.validator import Validator
from pipeline.rag_retriever import RAGRetriever
from pipeline.guardrails import Guardrails
from pipeline.dynamodb_store import DynamoDBStore

logger = logging.getLogger(__name__)


class ExtractionAgent:
    """LangGraph-style agent that orchestrates the extraction pipeline."""

    def __init__(self):
        self.textract = TextractClient()
        self.cleaner = TextCleaner()
        self.classifier = DocumentClassifier()
        self.rule_engine = RuleEngine()
        self.llm_extractor = LLMExtractor()
        self.consensus = ConsensusChecker()
        self.validator = Validator()
        self.rag = RAGRetriever()
        self.guardrails = Guardrails()
        self.db = DynamoDBStore()
        logger.info("Agent initialized with all workers")

    def run(self, document_id):
        """Agent decides what steps to take."""
        state = {"document_id": document_id, "status": "started"}

        state = self._step_ocr(state)
        state = self._step_clean(state)
        state = self._step_rag_store(state)
        state = self._step_extract(state)
        state = self._step_consensus(state)
        state = self._step_guardrails(state)
        state = self._step_validate(state)
        state = self._step_decide(state)
        state = self._step_store(state)

        
        return state

        # Step 1: OCR
        state = self._step_ocr(state)

        # Step 2: Clean
        state = self._step_clean(state)

        # Step 3: Extract with both methods
        state = self._step_extract(state)

        # Step 4: Consensus
        state = self._step_consensus(state)

        # Step 5: Validate
        state = self._step_validate(state)

        # Step 6: Agent decides - is result good enough?
        state = self._step_decide(state)

        return state

    def _step_ocr(self, state):
        """Agent step: Read document."""
        logger.info("Agent → Step 1: OCR")
        response = self.textract.process_document(state["document_id"])
        text_lines = [block['Text'] for block in response['Blocks'] if block.get('Text')]
        state["raw_text"] = ' '.join(text_lines)
        state["status"] = "ocr_complete"
        return state

    def _step_clean(self, state):
        """Agent step: Clean text."""
        logger.info("Agent → Step 2: Cleaning text")
        state["clean_text"] = self.cleaner.clean(state["raw_text"])
        state["status"] = "cleaned"
        return state

    def _step_rag_store(self, state):
        """Agent step: Store document chunks in vector DB."""
        logger.info("Agent → Step 3: Storing in vector DB (RAG)")
        chunks = self.rag.store_document(state["document_id"], state["clean_text"])
        state["chunks"] = chunks
        state["status"] = "stored_in_vectordb"
        return state
    
    def _step_extract(self, state):
        """Agent step: Run both extraction methods with RAG context."""
        logger.info("Agent → Step 4: Extracting (rules + LLM with RAG)")
        text = state["clean_text"]

        # RAG: Find relevant chunks for extraction
        relevant_chunks = self.rag.retrieve("borrower name loan amount interest rate term payment")
        rag_context = ' '.join(relevant_chunks)
        logger.info(f"RAG provided {len(relevant_chunks)} relevant chunks")

        classification = self.classifier.classify(text)
        state["rule_result"] = self.rule_engine.extract(text, classification["loan_type"])
        state["llm_result"] = self.llm_extractor.extract(rag_context)
        state["status"] = "extracted"
        return state

    def _step_consensus(self, state):
        """Agent step: Compare results."""
        logger.info("Agent → Step 4: Consensus check")
        state["final_result"] = self.consensus.check(state["rule_result"], state["llm_result"])
        state["status"] = "consensus_complete"
        return state
    
    def _step_guardrails(self, state):
        """Agent step: Check for hallucinations."""
        logger.info("Agent → Step 5: Guardrails check")
        state["guardrails"] = self.guardrails.check(state["final_result"], state["clean_text"])
        if not state["guardrails"]["passed"]:
            logger.warning("Guardrails failed — possible hallucinations detected")
        state["status"] = "guardrails_checked"
        return state

    def _step_validate(self, state):
        """Agent step: Validate results."""
        logger.info("Agent → Step 5: Validating")
        state["validation"] = self.validator.validate(state["final_result"])
        state["status"] = "validated"
        return state

    def _step_decide(self, state):
        """Agent step: Decide if results are good enough."""
        logger.info("Agent → Step 6: Decision")

        if not state["validation"]["valid"]:
            state["status"] = "needs_review"
            logger.warning("Agent decision: Send to human review")
            return state

        low_confidence = []
        for field, data in state["final_result"].items():
            if isinstance(data, dict) and data.get("confidence", 0) < 0.80:
                low_confidence.append(field)

        if low_confidence:
            state["status"] = "needs_review"
            logger.warning(f"Agent decision: Low confidence on {low_confidence}, send to human review")
        else:
            state["status"] = "approved"
            logger.info("Agent decision: All fields approved ✅")

        return state

    def _step_store(self, state):
        """Agent step: Store results in DynamoDB."""
        logger.info("Agent → Step 8: Storing in DynamoDB")
        self.db.store_result(state)
        state["status"] = "stored"
        return state