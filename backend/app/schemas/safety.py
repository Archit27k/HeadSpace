from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class RiskLevel(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    EMERGENCY = "Emergency"

class RiskAssessment(BaseModel):
    risk_level: RiskLevel = Field(..., description="Calculated overall risk level.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the risk assessment.")
    detected_signals: List[str] = Field(default_factory=list, description="List of detected risk signals (e.g., 'high_stress_emotion', 'suicidal_ideation').")
    supporting_evidence: List[str] = Field(default_factory=list, description="Evidence extracted from the conversation or journal supporting the assessment.")
    recommended_action: str = Field(..., description="Action recommended by the risk engine.")
    escalation_required: bool = Field(False, description="True if human intervention or emergency services are required.")
    requires_follow_up: bool = Field(False, description="True if the AI should check in on this later.")
    safety_category: str = Field(..., description="Broad category of risk (e.g., 'self_harm', 'severe_anxiety', 'general_distress').")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the assessment was made.")
