import pytest
from app.ai.safety.monitor import RiskEngine
from app.schemas.safety import RiskLevel
from app.ai.safety.intervention import InterventionEngine

def test_risk_engine_low_risk():
    state = {
        "messages": [{"role": "user", "content": "I am feeling okay today."}],
        "metadata": {"current_emotion": {"primary_emotion": "neutral", "risk_score": 0.1}}
    }
    assessment = RiskEngine.evaluate(state)
    assert assessment.risk_level == RiskLevel.LOW
    assert not assessment.escalation_required

def test_risk_engine_high_emotion_risk():
    state = {
        "messages": [{"role": "user", "content": "I am so overwhelmed."}],
        "metadata": {"current_emotion": {"primary_emotion": "anxiety", "risk_score": 0.8}}
    }
    assessment = RiskEngine.evaluate(state)
    assert assessment.risk_level == RiskLevel.HIGH
    assert assessment.requires_follow_up

def test_risk_engine_emergency():
    state = {
        "messages": [{"role": "user", "content": "I want to die."}],
        "metadata": {"current_emotion": {"primary_emotion": "despair", "risk_score": 0.95}}
    }
    assessment = RiskEngine.evaluate(state)
    assert assessment.risk_level == RiskLevel.EMERGENCY
    assert assessment.escalation_required

def test_intervention_routing():
    state = {
        "messages": [{"role": "user", "content": "I want to die."}],
        "metadata": {"current_emotion": {"primary_emotion": "despair", "risk_score": 0.95}}
    }
    assessment = RiskEngine.evaluate(state)
    tools = InterventionEngine.get_intervention_tools(assessment)
    assert len(tools) == 1
    assert tools[0]["name"] == "emergency_resource_tool"
