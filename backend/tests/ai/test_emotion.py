import pytest
from app.ai.emotion.classifier import MLflowEmotionService
from app.ai.emotion.schemas import EmotionResult
from app.ai.graph.nodes import planner, emotion_service

def test_emotion_service_mock_predictions():
    service = MLflowEmotionService()
    
    # Test sadness trigger
    res_sad = service.predict("I feel terrible and want to die")
    assert res_sad.primary_emotion == "sadness"
    assert res_sad.risk_score > 0.7
    assert res_sad.requires_follow_up is True
    
    # Test anger trigger
    res_angry = service.predict("I hate everything, I am so angry")
    assert res_angry.primary_emotion == "anger"
    
    # Test neutral/joy
    res_joy = service.predict("I had a good day")
    assert res_joy.primary_emotion == "joy"
    assert res_joy.risk_score < 0.3
    assert res_joy.requires_follow_up is False

def test_planner_crisis_routing():
    # Construct a state where emotion service just ran and found high risk
    from app.ai.emotion.schemas import EmotionResult
    from datetime import datetime
    
    high_risk_emotion = EmotionResult(
        primary_emotion="sadness",
        secondary_emotions=[],
        confidence=0.9,
        emotion_distribution={"sadness": 0.9},
        risk_score=0.85,
        requires_follow_up=True,
        model_version="test",
        inference_time_ms=10.0,
        timestamp=datetime.utcnow()
    )
    
    state = {
        "metadata": {"current_emotion": high_risk_emotion}
    }
    
    result = planner(state)
    assert result["current_intent"] == "crisis_support"
    assert result["metadata"]["planner_executed"] is True
