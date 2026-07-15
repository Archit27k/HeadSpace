from abc import ABC, abstractmethod
from typing import List
import numpy as np

class EmbeddingProvider(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def generate(self, texts: List[str]) -> np.ndarray:
        pass

class SentenceTransformerProvider(EmbeddingProvider):
    def __init__(self, model_name: str, device: str):
        self.model_name = model_name
        self.device = device
        self.model = None
        self.load_model()

    def load_model(self):
        from sentence_transformers import SentenceTransformer
        print(f"Loading SentenceTransformer model: {self.model_name} on {self.device}")
        self.model = SentenceTransformer(self.model_name, device=self.device)

    def generate(self, texts: List[str]) -> np.ndarray:
        if self.model is None:
            self.load_model()
        return self.model.encode(texts, show_progress_bar=True)
