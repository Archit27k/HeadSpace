from typing import Dict, Any

class ContextAggregator:
    """
    Extracts and formats context from the LangGraph state for the Wellness Engine.
    """
    
    @staticmethod
    def aggregate(state: Dict[str, Any]) -> str:
        """
        Combines Emotion, Journal, Memory, Conversation History, and Safety into a single formatted string.
        """
        metadata = state.get("metadata", {})
        
        # 1. Current Emotion
        emotion_res = metadata.get("current_emotion")
        emotion_str = "Unknown"
        if emotion_res:
            if isinstance(emotion_res, dict):
                emotion_str = f"{emotion_res.get('primary_emotion', 'Unknown')} (Risk: {emotion_res.get('risk_score', 0.0)})"
            else:
                emotion_str = f"{getattr(emotion_res, 'primary_emotion', 'Unknown')} (Risk: {getattr(emotion_res, 'risk_score', 0.0)})"
        
        # 2. Conversation History
        messages = state.get("messages", [])
        recent_messages = "\\n".join([f"{msg.get('role', 'unknown')}: {msg.get('content', '')}" for msg in messages[-3:]]) if messages else "None"
        
        # 3. Safety Assessment
        risk_dict = state.get("risk_assessment", {})
        risk_level = risk_dict.get("risk_level", "Low") if risk_dict else "Low"
        
        # 4. Memory (Extracted from state)
        memory = state.get("memory", {})
        long_term_facts = memory.get("long_term", []) if memory else []
        goals = memory.get("goals", []) if memory else []
        preferences = memory.get("preferences", []) if memory else []
        
        long_term_str = "\\n".join(long_term_facts) if long_term_facts else "None"
        goals_str = "\\n".join(goals) if goals else "None"
        preferences_str = "\\n".join(preferences) if preferences else "None"
        
        # 5. Planner Intent
        intent = state.get("current_intent", "Unknown")
        
        aggregated_context = f"""
[CURRENT CONTEXT]
Emotion State: {emotion_str}
Safety Risk Level: {risk_level}
Current Intent: {intent}

[RECENT CONVERSATION]
{recent_messages}

[LONG-TERM MEMORY]
Facts:
{long_term_str}

User Goals:
{goals_str}

User Preferences:
{preferences_str}
"""
        return aggregated_context
