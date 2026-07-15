import os
from typing import Dict, Any, List
from app.ai.ingestion.chunker import DocumentChunker
from app.ai.retrieval.qdrant import QdrantVectorStore
import logging

logger = logging.getLogger(__name__)

class DocumentIngestionPipeline:
    """
    End-to-End pipeline for reading files, extracting metadata, chunking, and pushing to vector store.
    """
    def __init__(self, qdrant_store: QdrantVectorStore):
        self.chunker = DocumentChunker()
        self.store = qdrant_store

    def _extract_text_pdf(self, file_path: str) -> str:
        """Extracts text from a PDF file using PyMuPDF."""
        try:
            import fitz # PyMuPDF
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except ImportError:
            logger.warning("PyMuPDF not installed. Cannot parse PDF.")
            return ""
        except Exception as e:
            logger.error(f"Failed to read PDF {file_path}: {e}")
            return ""

    def ingest_file(self, file_path: str, collection_name: str, base_metadata: Dict[str, Any] = None) -> int:
        """
        Reads a file, extracts text, chunks it, and ingests it into Qdrant.
        Returns the number of chunks ingested.
        """
        logger.info(f"Ingesting file {file_path} into collection {collection_name}")
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return 0
            
        text = ""
        metadata = base_metadata or {}
        metadata["source"] = os.path.basename(file_path)
        
        # Simple extension handling
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            text = self._extract_text_pdf(file_path)
        elif ext in [".md", ".txt"]:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            logger.error(f"Unsupported file type: {ext}")
            return 0
            
        if not text:
            logger.warning("No text extracted from file.")
            return 0
            
        # Chunk
        chunks = self.chunker.chunk_document(text, metadata)
        
        # Ingest
        if chunks:
            self.store.add_documents(chunks, collection_name)
            logger.info(f"Successfully ingested {len(chunks)} chunks.")
            
        return len(chunks)
