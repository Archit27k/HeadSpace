from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class CrossEncoderReranker:
    """
    Reranks documents using a Cross-Encoder model.
    Provides highly accurate semantic ranking at the cost of speed, 
    so it should only be run on top-k retrieved candidates.
    """
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        try:
            from sentence_transformers import CrossEncoder
            self.model = CrossEncoder(model_name)
            logger.info(f"Loaded CrossEncoder model: {model_name}")
        except ImportError:
            self.model = None
            logger.warning("sentence-transformers not installed. Reranker operates in Mock mode.")

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        if not documents:
            return []
            
        if not self.model:
            logger.info("Mock reranking - returning original order")
            return documents[:top_k]
            
        logger.info(f"Cross-Encoder reranking {len(documents)} documents for query: '{query}'")
        
        # Prepare pairs: (query, doc_text)
        pairs = [[query, doc.get("content", "")] for doc in documents]
        
        # Predict scores
        try:
            scores = self.model.predict(pairs)
            
            # Attach scores to documents
            for idx, doc in enumerate(documents):
                doc["rerank_score"] = float(scores[idx])
                
            # Sort by score descending
            ranked = sorted(documents, key=lambda x: x["rerank_score"], reverse=True)
            return ranked[:top_k]
        except Exception as e:
            logger.error(f"Reranking failed: {e}")
            return documents[:top_k]
