from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class EmbeddingInterface(ABC):
    """Abstract interface for text embedding models."""
    
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass

class VectorStoreInterface(ABC):
    """Abstract interface for Vector Stores with Hybrid Search support."""
    
    @abstractmethod
    def add_documents(self, documents: List[Dict[str, Any]], collection_name: str) -> None:
        """Adds documents with metadata and dense/sparse vectors to the store."""
        pass
        
    @abstractmethod
    def search(self, query: str, query_vector: List[float], collection_name: str, top_k: int = 5, filter_dict: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Standard dense vector search."""
        pass
        
    @abstractmethod
    def hybrid_search(self, query: str, query_vector: List[float], collection_name: str, top_k: int = 5, filter_dict: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Executes a Hybrid (Dense + Sparse/BM25) search, returning fused results."""
        pass

class RetrieverInterface(ABC):
    """Abstract interface for retrieving context for RAG."""
    
    @abstractmethod
    def retrieve(self, query: str, user_id: str, top_k: int = 5, collections: List[str] = None) -> List[Dict[str, Any]]:
        """High level retrieve function that orchestrates dense/sparse search and cross-encoder reranking."""
        pass
