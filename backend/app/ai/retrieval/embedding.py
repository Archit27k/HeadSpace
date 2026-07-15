from app.ai.retrieval.base import EmbeddingInterface
from typing import List
import logging

logger = logging.getLogger(__name__)

class SentenceTransformerEmbedding(EmbeddingInterface):
    """
    Embedding implementation using sentence-transformers.
    Defaults to all-MiniLM-L6-v2.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded SentenceTransformer model: {model_name}")
        except ImportError:
            self.model = None
            logger.warning("sentence-transformers not installed. Embedding operates in Mock mode.")

    def embed_text(self, text: str) -> List[float]:
        if not self.model:
            return [0.0] * 384
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if not self.model:
            return [[0.0] * 384 for _ in texts]
        return self.model.encode(texts).tolist()
