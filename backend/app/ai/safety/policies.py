from pydantic import BaseModel
from typing import List, Dict
from app.schemas.safety import RiskLevel

class SafetyPolicy(BaseModel):
    allowed_tools: List[str]
    override_planner: bool
    mandatory_intervention: bool
    system_prompt_override: str = ""

# Define the global safety policies
POLICIES: Dict[RiskLevel, SafetyPolicy] = {
    RiskLevel.LOW: SafetyPolicy(
        allowed_tools=["*"],
        override_planner=False,
        mandatory_intervention=False
    ),
    RiskLevel.MODERATE: SafetyPolicy(
        allowed_tools=["*"],
        override_planner=False,
        mandatory_intervention=False,
        system_prompt_override="The user is experiencing moderate stress. Be extra empathetic and supportive. Suggest a grounding exercise if appropriate."
    ),
    RiskLevel.HIGH: SafetyPolicy(
        allowed_tools=["grounding_tool", "breathing_tool", "wellness_resource_tool"],
        override_planner=True,
        mandatory_intervention=True,
        system_prompt_override="The user is in high distress. Do not probe deeply into trauma. Offer immediate grounding techniques and validate their feelings."
    ),
    RiskLevel.EMERGENCY: SafetyPolicy(
        allowed_tools=["emergency_resource_tool"],
        override_planner=True,
        mandatory_intervention=True,
        system_prompt_override="CRITICAL: The user is in an emergency state (risk of self-harm or severe crisis). You MUST prioritize their safety above all else. Provide emergency contact resources gently but firmly. Do not attempt to counsel or solve their crisis."
    )
}

def get_policy(level: RiskLevel) -> SafetyPolicy:
    return POLICIES.get(level, POLICIES[RiskLevel.LOW])
