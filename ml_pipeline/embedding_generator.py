from .config import config
from .embedding_provider import SentenceTransformerProvider
import numpy as np

class EmbeddingGenerator:
    def __init__(self):
        # We can easily swap out the provider here or use a factory pattern based on config
        self.provider = SentenceTransformerProvider(
            model_name=config.EMBEDDING_MODEL,
            device=config.DEVICE
        )
        
    def generate(self, texts: list[str]) -> np.ndarray:
        """
        Generates dense embeddings for a list of texts using the configured provider.
        """
        print(f"Generating embeddings for {len(texts)} texts...")
        return self.provider.generate(texts)
