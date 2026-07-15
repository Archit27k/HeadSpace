from typing import Dict, Any, List
from app.schemas.safety import RiskAssessment, RiskLevel
import logging

logger = logging.getLogger(__name__)

class RiskEngine:
    """
    Evaluates evidence from multiple sources to compute a comprehensive risk assessment.
    """
    
    @staticmethod
    def evaluate(state: Dict[str, Any]) -> RiskAssessment:
        """
        Combines Emotion Intelligence, Conversation History, and Planner Decisions
        to produce a structured RiskAssessment.
        """
        signals = []
        evidence = []
        
        # 1. Analyze Emotion Output
        metadata = state.get("metadata", {})
        emotion_res = metadata.get("current_emotion", None)
        risk_score = 0.0
        
        if emotion_res:
            # Depending on how the EmotionResult is structured in state.
            # Assuming it might be a dict or object. Let's handle both.
            if isinstance(emotion_res, dict):
                r_score = emotion_res.get("risk_score", 0.0)
                primary = emotion_res.get("primary_emotion", "unknown")
            else:
                r_score = getattr(emotion_res, "risk_score", 0.0)
                primary = getattr(emotion_res, "primary_emotion", "unknown")
                
            risk_score = r_score
            if r_score > 0.7:
                signals.append("high_emotion_risk")
                evidence.append(f"Detected primary emotion '{primary}' with high risk score: {r_score}")

        # 2. Analyze Conversation History (Explicit Risk Phrases)
        messages = state.get("messages", [])
        latest_msg = messages[-1].get("content", "").lower() if messages else ""
        
        emergency_phrases = ["kill myself", "want to die", "end it all", "suicide", "hurt myself"]
        high_risk_phrases = ["can't take this", "worthless", "pointless", "give up"]
        
        has_emergency = any(phrase in latest_msg for phrase in emergency_phrases)
        has_high_risk = any(phrase in latest_msg for phrase in high_risk_phrases)
        
        if has_emergency:
            signals.append("explicit_emergency_phrase")
            evidence.append("User expressed explicit thoughts of self-harm or suicide.")
            risk_score = max(risk_score, 1.0)
        elif has_high_risk:
            signals.append("high_risk_phrase")
            evidence.append("User expressed feelings of hopelessness or severe distress.")
            risk_score = max(risk_score, 0.8)
            
        # 3. Analyze Planner Intent
        intent = state.get("current_intent", "")
        if intent == "crisis_support":
            signals.append("crisis_intent_detected")
            risk_score = max(risk_score, 0.75)

        # 4. Map to RiskLevel
        risk_level = RiskLevel.LOW
        escalation = False
        follow_up = False
        action = "continue_normal_monitoring"
        category = "general_wellness"
        
        if risk_score >= 0.9 or has_emergency:
            risk_level = RiskLevel.EMERGENCY
            escalation = True
            action = "trigger_emergency_protocol"
            category = "severe_crisis"
        elif risk_score >= 0.7:
            risk_level = RiskLevel.HIGH
            follow_up = True
            action = "trigger_high_risk_intervention"
            category = "high_distress"
        elif risk_score >= 0.4:
            risk_level = RiskLevel.MODERATE
            action = "suggest_grounding_or_coping"
            category = "moderate_stress"
            
        return RiskAssessment(
            risk_level=risk_level,
            confidence=0.85, # Simplification
            detected_signals=signals,
            supporting_evidence=evidence,
            recommended_action=action,
            escalation_required=escalation,
            requires_follow_up=follow_up,
            safety_category=category
        )
