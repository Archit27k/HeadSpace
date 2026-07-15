from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from uuid import UUID

from app.models.database import get_db
from app.core.security import get_current_user
from app.models.models import User, LongTermMemoryItem

router = APIRouter()

@router.get("/")
async def get_memory_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(LongTermMemoryItem).filter(LongTermMemoryItem.user_id == current_user.id).order_by(LongTermMemoryItem.created_at.desc()).all()
    # Manual serialization since we don't have a specific schema yet
    return [
        {
            "id": str(item.id),
            "content": item.fact_text,
            "category": item.category,
            "importance_score": item.relevance_score,
            "created_at": item.created_at.isoformat() if item.created_at else None
        }
        for item in items
    ]

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory_item(item_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(LongTermMemoryItem).filter(LongTermMemoryItem.id == item_id, LongTermMemoryItem.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Memory item not found")
    
    db.delete(item)
    db.commit()
