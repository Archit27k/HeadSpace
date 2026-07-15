from app.schemas.safety import RiskAssessment, RiskLevel
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class InterventionEngine:
    """
    Selects the appropriate intervention tools and actions based on the RiskAssessment.
    """
    
    @staticmethod
    def get_intervention_tools(assessment: RiskAssessment) -> List[Dict[str, Any]]:
        """
        Determines which safety tools to invoke based on risk level.
        Returns a list of tool execution requests for the ToolExecutionEngine.
        """
        tools = []
        
        if assessment.risk_level == RiskLevel.EMERGENCY:
            logger.warning("InterventionEngine: Triggering Emergency Resource Tool")
            tools.append({
                "name": "emergency_resource_tool",
                "arguments": {"reason": "Explicit risk detected. Providing hotline information."}
            })
            
        elif assessment.risk_level == RiskLevel.HIGH:
            logger.info("InterventionEngine: Triggering Grounding Tool")
            tools.append({
                "name": "grounding_tool",
                "arguments": {"technique": "5-4-3-2-1"}
            })
            
        elif assessment.risk_level == RiskLevel.MODERATE:
            # Maybe we don't force a tool, but we could suggest breathing
            pass
            
        return tools
