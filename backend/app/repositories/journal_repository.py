from sqlalchemy.orm import Session
from app.models import models
from app.schemas import journal as journal_schema
from uuid import UUID
from typing import List

class JournalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, entry_id: UUID) -> models.JournalEntry:
        return self.db.query(models.JournalEntry).filter(models.JournalEntry.id == entry_id).first()

    def get_all_for_user(self, user_id: UUID) -> List[models.JournalEntry]:
        return self.db.query(models.JournalEntry).filter(models.JournalEntry.user_id == user_id).order_by(models.JournalEntry.created_at.desc()).all()

    def create(self, entry: journal_schema.JournalEntryCreate, user_id: UUID) -> models.JournalEntry:
        db_entry = models.JournalEntry(
            user_id=user_id,
            title=entry.title,
            content=entry.content
        )
        self.db.add(db_entry)
        self.db.commit()
        self.db.refresh(db_entry)
        return db_entry

    def update(self, db_entry: models.JournalEntry, entry_update: journal_schema.JournalEntryUpdate) -> models.JournalEntry:
        if entry_update.title is not None:
            db_entry.title = entry_update.title
        if entry_update.content is not None:
            db_entry.content = entry_update.content
        self.db.commit()
        self.db.refresh(db_entry)
        return db_entry
        
    def delete(self, db_entry: models.JournalEntry):
        self.db.delete(db_entry)
        self.db.commit()
