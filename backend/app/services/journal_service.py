from app.repositories.journal_repository import JournalRepository
from app.schemas import journal as journal_schema
from app.models.models import JournalEntry
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

class JournalService:
    def __init__(self, db: Session):
        self.repo = JournalRepository(db)

    def get_entries(self, user_id: UUID) -> List[JournalEntry]:
        return self.repo.get_all_for_user(user_id)

    def get_entry(self, entry_id: UUID, user_id: UUID) -> JournalEntry:
        entry = self.repo.get_by_id(entry_id)
        if not entry or entry.user_id != user_id:
            return None
        return entry

    def create_entry(self, user_id: UUID, entry: journal_schema.JournalEntryCreate) -> JournalEntry:
        return self.repo.create(entry, user_id)

    def update_entry(self, user_id: UUID, entry_id: UUID, entry_update: journal_schema.JournalEntryUpdate) -> JournalEntry:
        entry = self.get_entry(entry_id, user_id)
        if not entry:
            return None
        return self.repo.update(entry, entry_update)

    def delete_entry(self, user_id: UUID, entry_id: UUID) -> bool:
        entry = self.get_entry(entry_id, user_id)
        if not entry:
            return False
        self.repo.delete(entry)
        return True
