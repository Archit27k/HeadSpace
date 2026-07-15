from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class EmotionResult(BaseModel):
    """
    Structured output from the MLflow Emotion Classifier.
    Used by the LangGraph planner and prompt builders.
    """
    primary_emotion: str
    secondary_emotions: List[str]
    confidence: float
    emotion_distribution: Dict[str, float]
    risk_score: float # 0.0 to 1.0 (1.0 = high risk/crisis)
    requires_follow_up: bool
    model_version: str
    inference_time_ms: float
    timestamp: datetime
