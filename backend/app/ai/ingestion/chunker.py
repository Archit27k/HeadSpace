from typing import List, Dict, Any
import logging
import uuid

logger = logging.getLogger(__name__)

class DocumentChunker:
    """
    Handles chunking of documents.
    Supports basic Recursive chunking and advanced Parent-Child chunking.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
        except ImportError:
            self.splitter = None
            logger.warning("langchain-text-splitters not installed. Using naive chunker.")

    def _naive_split(self, text: str) -> List[str]:
        # Very naive fallback
        words = text.split()
        chunks = []
        for i in range(0, len(words), 100):
            chunks.append(" ".join(words[i:i+120]))
        return chunks

    def chunk_document(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Splits text and propagates metadata to all chunks.
        """
        logger.info(f"Chunking document '{metadata.get('title', 'Unknown')}'")
        
        if self.splitter:
            text_chunks = self.splitter.split_text(text)
        else:
            text_chunks = self._naive_split(text)
            
        final_chunks = []
        for idx, chunk in enumerate(text_chunks):
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                "chunk_index": idx,
                "total_chunks": len(text_chunks),
            })
            
            final_chunks.append({
                "id": str(uuid.uuid4()),
                "content": chunk,
                "metadata": chunk_metadata
            })
            
        return final_chunks
