from sqlalchemy.orm import Session
from app.models import models
from app.schemas import chat as chat_schema
from uuid import UUID
from typing import List

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_session(self, session_id: UUID) -> models.Session:
        return self.db.query(models.Session).filter(models.Session.id == session_id).first()
        
    def get_sessions_for_user(self, user_id: UUID) -> List[models.Session]:
        return self.db.query(models.Session).filter(models.Session.user_id == user_id).order_by(models.Session.started_at.desc()).all()
        
    def create_session(self, user_id: UUID) -> models.Session:
        db_session = models.Session(user_id=user_id)
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def create_conversation(self, session_id: UUID, summary: str = None) -> models.Conversation:
        db_conv = models.Conversation(session_id=session_id, summary=summary)
        self.db.add(db_conv)
        self.db.commit()
        self.db.refresh(db_conv)
        return db_conv
        
    def get_conversations_for_session(self, session_id: UUID) -> List[models.Conversation]:
        return self.db.query(models.Conversation).filter(models.Conversation.session_id == session_id).all()

    def get_conversation(self, conversation_id: UUID) -> models.Conversation:
        return self.db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

    def add_message(self, conversation_id: UUID, role: str, content: str) -> models.Message:
        db_message = models.Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
