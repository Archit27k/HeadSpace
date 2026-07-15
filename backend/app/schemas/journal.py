from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class JournalEntryBase(BaseModel):
    title: str
    content: str

class JournalEntryCreate(JournalEntryBase):
    pass

class JournalEntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class JournalEntryResponse(JournalEntryBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

from typing import List, Dict, Any

class MemoryUpdateSuggestion(BaseModel):
    category: str
    fact_text: str
    relevance_score: float = 1.0

class PlannerMetadata(BaseModel):
    requires_crisis_intervention: bool = False
    suggested_follow_up: Optional[str] = None

class JournalAnalysisOutput(BaseModel):
    summary: str
    primary_emotions: List[str]
    secondary_emotions: List[str] = []
    themes: List[str] = []
    key_events: List[str] = []
    stress_score: int
    cognitive_distortions: List[str] = []
    reflection_questions: List[str] = []
    recommended_coping_strategies: List[str] = []
    suggested_action_items: List[str] = []
    memory_updates: List[MemoryUpdateSuggestion] = []
    planner_metadata: PlannerMetadata
    confidence: float
