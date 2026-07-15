from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
import fitz # PyMuPDF
import io
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

from app.models.database import get_db
from app.core.security import get_current_user
from app.models.models import User
from app.ai.retrieval.qdrant import QdrantVectorStore

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        content = await file.read()
        
        # 1. Extract text
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
            
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
            
        # 2. Chunk text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)
        
        # 3. Index chunks to Qdrant
        vector_store = QdrantVectorStore()
        # Ensure collection exists
        vector_store._ensure_collection("user_documents")
        
        points = []
        for i, chunk in enumerate(chunks):
            metadata = {
                "user_id": str(current_user.id),
                "source": file.filename,
                "chunk_index": i,
                "type": "document"
            }
            # QdrantVectorStore.upsert expects documents with content and metadata
            points.append({
                "content": chunk,
                "metadata": metadata
            })
            
        # Bulk index
        # Looking at QdrantVectorStore implementation, it probably has an `add_documents` or similar
        # If it doesn't have a bulk add interface exposed, we will add them one by one.
        for point in points:
            vector_store.upsert(
                collection_name="user_documents",
                content=point["content"],
                metadata=point["metadata"]
            )
            
        return {"message": f"Successfully indexed {len(chunks)} chunks from {file.filename}", "chunks_count": len(chunks)}
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
