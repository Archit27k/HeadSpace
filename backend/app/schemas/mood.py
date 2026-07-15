from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class MoodLogBase(BaseModel):
    score: int
    primary_emotion: str
    notes: Optional[str] = None

class MoodLogCreate(MoodLogBase):
    pass

class MoodLogResponse(MoodLogBase):
    id: UUID
    user_id: UUID
    logged_at: datetime

    model_config = ConfigDict(from_attributes=True)
