from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendationItem(BaseModel):
    category: str = Field(..., description="Category of the recommendation (e.g., 'Stress Reduction', 'Sleep Hygiene', 'Mindfulness').")
    title: str = Field(..., description="Short, actionable title.")
    description: str = Field(..., description="Detailed description of the recommendation.")
    estimated_duration: str = Field(..., description="Estimated time to complete (e.g., '5 mins', '10 mins').")

class WellnessEngineOutput(BaseModel):
    recommendations: List[RecommendationItem] = Field(default_factory=list, description="List of generated personalized wellness recommendations.")
    priority: str = Field(..., description="Overall priority of these recommendations (Low, Medium, High).")
    reasoning: str = Field(..., description="Explanation of why these recommendations were chosen based on the user's context.")
    supporting_evidence: List[str] = Field(default_factory=list, description="Specific context points (e.g., 'User reported high stress in journal') supporting the reasoning.")
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0.")
    follow_up_questions: List[str] = Field(default_factory=list, description="Suggested questions to ask the user to guide them.")
    action_plan: List[str] = Field(default_factory=list, description="A step-by-step summary plan for the user.")
    memory_suggestions: List[str] = Field(default_factory=list, description="Items to persist to long-term memory (e.g., 'User likes mindfulness exercises').")
