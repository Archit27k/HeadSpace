import pytest
from app.ai.wellness.context import ContextAggregator
from app.ai.wellness.validator import SafetyValidator
from app.schemas.wellness import WellnessEngineOutput, RecommendationItem
from app.schemas.safety import RiskLevel

def test_context_aggregator():
    state = {
        "messages": [{"role": "user", "content": "I am feeling stressed."}],
        "metadata": {"current_emotion": {"primary_emotion": "stress", "risk_score": 0.4}},
        "memory": {"long_term": ["User works long hours."]},
        "current_intent": "seek_guidance",
        "risk_assessment": {"risk_level": "Moderate"}
    }
    context = ContextAggregator.aggregate(state)
    assert "stress (Risk: 0.4)" in context
    assert "Moderate" in context
    assert "seek_guidance" in context
    assert "User works long hours." in context

def test_safety_validator_low_risk():
    output = WellnessEngineOutput(
        recommendations=[RecommendationItem(category="Mindfulness", title="Meditate", description="Breathe", estimated_duration="5 min")],
        priority="Low",
        reasoning="User asked for meditation.",
        confidence=0.9
    )
    state = {"risk_assessment": {"risk_level": RiskLevel.LOW}}
    
    validated = SafetyValidator.validate(output, state)
    assert len(validated.recommendations) == 1

def test_safety_validator_emergency_risk():
    output = WellnessEngineOutput(
        recommendations=[RecommendationItem(category="Mindfulness", title="Meditate", description="Breathe", estimated_duration="5 min")],
        priority="Low",
        reasoning="User asked for meditation.",
        confidence=0.9
    )
    state = {"risk_assessment": {"risk_level": RiskLevel.EMERGENCY}}
    
    validated = SafetyValidator.validate(output, state)
    assert len(validated.recommendations) == 0
    assert "safety override" in validated.reasoning.lower()
