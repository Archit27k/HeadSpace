from typing import List, Dict, Any
from app.ai.prompts.base import BasePromptTemplate

class SystemChatPrompt(BasePromptTemplate):
    """
    The core system prompt for the mental health companion.
    """
    
    @property
    def name(self) -> str:
        return "system_chat"
        
    @property
    def description(self) -> str:
        return "Core persona and rules for the HeadSpace AI companion."
        
    @property
    def version(self) -> str:
        return "1.0.0"
        
    @property
    def input_variables(self) -> List[str]:
        return ["user_name", "context_str", "rules"]
        
    def render(self, **kwargs) -> str:
        for var in self.input_variables:
            if var not in kwargs:
                raise ValueError(f"Missing required variable for {self.name}: {var}")
                
        template = f"""You are HeadSpace AI, an empathetic, evidence-based mental health companion.

You are currently talking to {kwargs['user_name']}.

<CONTEXT>
{kwargs['context_str']}
</CONTEXT>

<RULES>
{kwargs['rules']}
</RULES>

Always respond with empathy, warmth, and professionalism. Do not diagnose or prescribe medication.
"""
        return template
