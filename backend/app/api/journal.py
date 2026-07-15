from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.models.database import get_db
from app.core.security import get_current_user
from app.services.journal_service import JournalService
from app.schemas.journal import JournalEntryResponse, JournalEntryCreate, JournalEntryUpdate
from app.models.models import User

router = APIRouter()

@router.get("/", response_model=List[JournalEntryResponse])
async def get_entries(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = JournalService(db)
    return service.get_entries(current_user.id)

from fastapi import BackgroundTasks

async def process_journal_entry(user_id: str, entry_id: str, entry_content: str):
    from app.ai.graph.builder import build_orchestration_graph
    try:
        graph = build_orchestration_graph()
        initial_state = {
            "conversation_id": entry_id,
            "user_id": user_id,
            "messages": [{"role": "user", "content": f"New journal entry: {entry_content}"}],
            "current_intent": "journal_entry",
            "emotion": {},
            "risk_assessment": None,
            "retrieved_context": [],
            "planner_decisions": {},
            "memory": {},
            "selected_tools": [],
            "tool_outputs": [],
            "validation_results": {},
            "metadata": {"latest_message": entry_content},
            "execution_trace": []
        }
        await graph.ainvoke(initial_state)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Journal Intelligence failed: {e}")

@router.post("/", response_model=JournalEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_entry(entry: JournalEntryCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = JournalService(db)
    new_entry = service.create_entry(current_user.id, entry)
    background_tasks.add_task(process_journal_entry, str(current_user.id), str(new_entry.id), entry.content)
    return new_entry

@router.get("/{entry_id}", response_model=JournalEntryResponse)
async def get_entry(entry_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = JournalService(db)
    entry = service.get_entry(entry_id, current_user.id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.put("/{entry_id}", response_model=JournalEntryResponse)
async def update_entry(entry_id: UUID, entry_update: JournalEntryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = JournalService(db)
    entry = service.update_entry(current_user.id, entry_id, entry_update)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(entry_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = JournalService(db)
    success = service.delete_entry(current_user.id, entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entry not found")
