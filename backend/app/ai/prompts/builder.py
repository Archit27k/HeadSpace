from typing import Dict, Any, List
from app.ai.prompts.registry import prompt_registry
import logging

logger = logging.getLogger(__name__)

class ContextBuilder:
    """
    Merges different sources of state (history, memory, user profile) 
    into structured context strings for the prompt.
    """
    @staticmethod
    def build_context_string(memory_items: List[Dict[str, Any]]) -> str:
        """Converts retrieved ranked memory items into a readable string format."""
        if not memory_items:
            return "No relevant past context found."
            
        context_lines = []
        for item in memory_items:
            t = item.get("type", "unknown")
            content = item.get("content", "")
            context_lines.append(f"[{t.upper()}]: {content}")
            
        return "\n".join(context_lines)
        
    @staticmethod
    def get_system_rules(intent: str) -> str:
        """Fetches dynamic rules based on current intent (e.g. crisis vs general)."""
        if intent == "crisis_support":
            return "IMMEDIATE RULE: Provide crisis helpline numbers immediately. Do not attempt to de-escalate without offering professional resources."
        return "1. Be empathetic. 2. Ask open-ended questions. 3. Validate their feelings."

class PromptBuilder:
    """
    Uses the ContextBuilder and PromptRegistry to assemble the final 
    system instructions and full prompt package for the LLM.
    """
    @staticmethod
    def build_system_prompt(template_name: str, state: Dict[str, Any], user_metadata: Dict[str, Any] = None) -> str:
        """
        Assembles the system prompt.
        """
        logger.info(f"Building system prompt using template: {template_name}")
        
        template = prompt_registry.get(template_name)
        
        # Build context blocks
        memory_items = state.get("memory", {}).get("ranked_context", [])
        context_str = ContextBuilder.build_context_string(memory_items)
        
        intent = state.get("current_intent", "general_chat")
        rules_str = ContextBuilder.get_system_rules(intent)
        
        user_name = user_metadata.get("first_name", "User") if user_metadata else "User"
        
        # Render prompt
        rendered = template.render(
            user_name=user_name,
            context_str=context_str,
            rules=rules_str
        )
        
        return rendered
