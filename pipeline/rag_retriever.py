import logging
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Chunks documents, creates embeddings, and retrieves relevant sections."""

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " "]
        )
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks = []
        self.embeddings = None
        logger.info("RAG Retriever initialized")

    def store_document(self, document_id, text):
        """Split text into chunks and create embeddings."""
        self.chunks = self.splitter.split_text(text)
        logger.info(f"Split document into {len(self.chunks)} chunks")

        self.embeddings = self.embedding_model.encode(self.chunks)
        logger.info(f"Created embeddings for {len(self.chunks)} chunks")
        return self.chunks

    def retrieve(self, query, n_results=3):
        """Find the most relevant chunks for a question."""
        if not self.chunks:
            return []

        query_embedding = self.embedding_model.encode([query])

        # Calculate similarity scores
        scores = np.dot(self.embeddings, query_embedding.T).flatten()
        top_indices = np.argsort(scores)[-n_results:][::-1]

        results = [self.chunks[i] for i in top_indices]
        logger.info(f"Retrieved {len(results)} relevant chunks for: '{query}'")
        return results

