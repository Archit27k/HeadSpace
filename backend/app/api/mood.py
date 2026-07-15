from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.models.database import get_db
from app.core.security import get_current_user
from app.schemas.mood import MoodLogCreate, MoodLogResponse
from app.models.models import User, MoodLog

router = APIRouter()

@router.get("/", response_model=List[MoodLogResponse])
async def get_mood_logs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logs = db.query(MoodLog).filter(MoodLog.user_id == current_user.id).order_by(MoodLog.logged_at.desc()).all()
    return logs

from fastapi import BackgroundTasks

def process_mood_emotion(user_id: str, notes: str):
    if not notes:
        return
    
    try:
        from app.models.database import SessionLocal
        from app.models.models import EmotionTimelineItem
        from app.ai.emotion.classifier import MLflowEmotionService
        import uuid
        
        db = SessionLocal()
        classifier = MLflowEmotionService()
        result = classifier.predict(notes)
        
        emo_item = EmotionTimelineItem(
            user_id=uuid.UUID(user_id),
            primary_emotion=result.primary_emotion,
            secondary_emotions=result.secondary_emotions,
            confidence=result.confidence,
            risk_score=result.risk_score,
            intensity=result.intensity,
            context_tags=result.context_tags
        )
        db.add(emo_item)
        db.commit()
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Failed to process mood emotion: {e}")
    finally:
        if 'db' in locals():
            db.close()

@router.post("/", response_model=MoodLogResponse, status_code=status.HTTP_201_CREATED)
async def create_mood_log(mood: MoodLogCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_mood = MoodLog(
        user_id=current_user.id,
        score=mood.score,
        primary_emotion=mood.primary_emotion,
        notes=mood.notes
    )
    db.add(db_mood)
    db.commit()
    db.refresh(db_mood)
    
    if mood.notes:
        background_tasks.add_task(process_mood_emotion, str(current_user.id), mood.notes)
        
    return db_mood
