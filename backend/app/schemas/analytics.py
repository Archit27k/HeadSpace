from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TrendData(BaseModel):
    date: str = Field(..., description="Date of the data point.")
    score: float = Field(..., description="Numerical score (e.g., stress level, emotion risk).")
    category: str = Field(..., description="Category of the trend (e.g., 'Stress', 'Mood').")

class Insight(BaseModel):
    title: str = Field(..., description="Title of the insight.")
    description: str = Field(..., description="Detailed explanation of the insight.")
    confidence: float = Field(..., description="Confidence score.")
    insight_type: str = Field(..., description="Type of insight (e.g., 'Behavior Pattern', 'Recurring Stressor').")

class ExplainabilityReport(BaseModel):
    recommendation_id: str = Field(..., description="ID or title of the recommendation.")
    evidence_used: List[str] = Field(..., description="List of direct evidence used to generate the recommendation.")
    relevant_journals: List[str] = Field(default_factory=list, description="IDs or dates of relevant journal entries.")
    confidence: float = Field(..., description="Confidence level of the recommendation.")
    reasoning: str = Field(..., description="Plain-text explanation of the AI's reasoning process.")

class DashboardSummary(BaseModel):
    trends: List[TrendData] = Field(default_factory=list)
    insights: List[Insight] = Field(default_factory=list)
    recent_explanations: List[ExplainabilityReport] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
