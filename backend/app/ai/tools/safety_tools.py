from pydantic import BaseModel, Field
from typing import Any
import logging
from app.ai.tools.base import BaseTool

logger = logging.getLogger(__name__)

class EmergencyResourceInput(BaseModel):
    reason: str = Field(..., description="Reason for triggering the emergency resource tool.")

class EmergencyResourceOutput(BaseModel):
    message: str = Field(..., description="The emergency message and hotline info provided to the user.")

class EmergencyResourceTool(BaseTool):
    name: str = "emergency_resource_tool"
    description: str = "Provides emergency contact information and hotlines for users in crisis."
    version: str = "1.0.0"
    
    input_schema = EmergencyResourceInput
    output_schema = EmergencyResourceOutput
    
    def _run(self, **kwargs) -> Any:
        raise NotImplementedError
        
    async def _arun(self, **kwargs) -> Any:
        # In a real app, this might pull localized hotlines based on user profile
        message = (
            "I'm really sorry you're feeling this way, but please know you're not alone. "
            "If you're in immediate danger or experiencing a mental health crisis, please reach out for help right away.\n\n"
            "- National Suicide Prevention Lifeline: 988\n"
            "- Crisis Text Line: Text HOME to 741741\n"
            "- Emergency Services: 911\n\n"
            "Please contact one of these resources. They are available 24/7."
        )
        return {"message": message}

class GroundingInput(BaseModel):
    technique: str = Field("5-4-3-2-1", description="The grounding technique to suggest.")

class GroundingOutput(BaseModel):
    exercise: str = Field(..., description="The text of the grounding exercise.")

class GroundingTool(BaseTool):
    name: str = "grounding_tool"
    description: str = "Provides a grounding exercise to help reduce severe anxiety or panic."
    version: str = "1.0.0"
    
    input_schema = GroundingInput
    output_schema = GroundingOutput
    
    def _run(self, **kwargs) -> Any:
        raise NotImplementedError
        
    async def _arun(self, **kwargs) -> Any:
        technique = kwargs.get("technique", "5-4-3-2-1")
        
        if technique == "5-4-3-2-1":
            exercise = (
                "Let's try a quick grounding exercise together called the 5-4-3-2-1 method. "
                "Take a deep breath. Now, look around you and identify:\n"
                "- 5 things you can see\n"
                "- 4 things you can physically feel\n"
                "- 3 things you can hear\n"
                "- 2 things you can smell\n"
                "- 1 thing you can taste\n"
                "Take your time."
            )
        else:
            exercise = "Let's take a moment to ground ourselves. Focus on the feeling of your feet on the floor and take three slow, deep breaths."
            
        return {"exercise": exercise}
