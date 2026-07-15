from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.models.database import get_db
from app.core.security import get_current_user
from app.models.models import User
from app.ai.tools.wellness_intelligence import WellnessIntelligenceTool

router = APIRouter()

@router.get("/")
async def get_recommendations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tool = WellnessIntelligenceTool()
    
    from app.models.models import EmotionTimelineItem, LongTermMemoryItem, JournalEntry
    import uuid
    uid = uuid.UUID(str(current_user.id))
    
    # 1. Fetch current emotion (latest)
    latest_emotion = db.query(EmotionTimelineItem).filter(EmotionTimelineItem.user_id == uid).order_by(EmotionTimelineItem.timestamp.desc()).first()
    emotion_dict = None
    if latest_emotion:
        emotion_dict = {
            "primary_emotion": latest_emotion.primary_emotion,
            "risk_score": float(latest_emotion.risk_score)
        }
        
    # 2. Fetch memory facts
    memories = db.query(LongTermMemoryItem).filter(LongTermMemoryItem.user_id == uid).all()
    long_term = [m.fact_text for m in memories if m.category == "Fact"]
    goals = [m.fact_text for m in memories if m.category == "Goal"]
    preferences = [m.fact_text for m in memories if m.category == "Preference"]
    
    state = {
        "user_id": str(current_user.id),
        "messages": [], # We could fetch chat history here if we wanted
        "metadata": {
            "current_emotion": emotion_dict
        },
        "memory": {
            "long_term": long_term,
            "goals": goals,
            "preferences": preferences
        },
        "current_intent": "wellness_check"
    }
    
    import json
    result = await tool._arun(state_dump=json.dumps(state))
    return result
