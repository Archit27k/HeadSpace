from typing import Dict, Any, List

class PlannerMetrics:
    """
    Evaluates the accuracy of LangGraph planner decisions.
    """
    
    @staticmethod
    def evaluate_routing(predicted_intent: str, expected_intent: str) -> Dict[str, Any]:
        """
        Evaluates whether the planner selected the correct routing intent.
        """
        is_correct = (predicted_intent == expected_intent)
        return {
            "metric": "routing_accuracy",
            "score": 1.0 if is_correct else 0.0,
            "predicted": predicted_intent,
            "expected": expected_intent
        }

class EmotionMetrics:
    """
    Evaluates Emotion Intelligence integration.
    """
    
    @staticmethod
    def evaluate_emotion(predicted_emotion: str, expected_emotion: str) -> Dict[str, Any]:
        is_correct = (predicted_emotion == expected_emotion)
        return {
            "metric": "emotion_accuracy",
            "score": 1.0 if is_correct else 0.0,
            "predicted": predicted_emotion,
            "expected": expected_emotion
        }
