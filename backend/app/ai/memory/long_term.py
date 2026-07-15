from app.ai.memory.base import BaseMemory
from app.models.models import LongTermMemoryItem
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class LongTermMemory(BaseMemory):
    """
    Handles structured, persistent user facts stored in PostgreSQL.
    """
    def __init__(self, db: Session):
        self.db = db

    def store(self, user_id: UUID, session_id: Optional[UUID], data: Dict[str, Any], **kwargs) -> LongTermMemoryItem:
        logger.info(f"Storing long term memory for user {user_id}: {data}")
        item = LongTermMemoryItem(
            user_id=user_id,
            category=data.get("category", "general"),
            fact_text=data.get("fact_text", ""),
            relevance_score=data.get("relevance_score", 1.0)
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def retrieve(self, user_id: UUID, session_id: Optional[UUID], query: str = None, **kwargs) -> List[Dict[str, Any]]:
        logger.info(f"Retrieving long term memory for user {user_id}")
        # Basic SQL retrieval. A full implementation could do keyword matching on `query`
        items = self.db.query(LongTermMemoryItem).filter(LongTermMemoryItem.user_id == user_id).order_by(LongTermMemoryItem.relevance_score.desc()).limit(10).all()
        
        return [
            {
                "type": "long_term",
                "content": item.fact_text,
                "category": item.category,
                "relevance_score": item.relevance_score,
                "metadata": {"id": str(item.id)}
            }
            for item in items
        ]

    def update(self, memory_id: UUID, data: Dict[str, Any], **kwargs) -> LongTermMemoryItem:
        item = self.db.query(LongTermMemoryItem).filter(LongTermMemoryItem.id == memory_id).first()
        if not item:
            return None
        
        if "fact_text" in data:
            item.fact_text = data["fact_text"]
        if "relevance_score" in data:
            item.relevance_score = data["relevance_score"]
            
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, memory_id: UUID, **kwargs) -> bool:
        item = self.db.query(LongTermMemoryItem).filter(LongTermMemoryItem.id == memory_id).first()
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
