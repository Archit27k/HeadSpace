import time
from typing import Dict, Any
from app.ai.graph.state import GraphState
from app.ai.safety.monitor import RiskEngine
from app.ai.graph.nodes import _record_trace

def safety_monitor(state: GraphState) -> Dict[str, Any]:
    """
    Independent safety node that executes the Risk Engine
    to produce a structured RiskAssessment.
    Executes BEFORE the planner.
    """
    start_time = time.time()
    
    # Generate risk assessment
    risk_assessment = RiskEngine.evaluate(state)
    
    metadata_update = state.get("metadata", {})
    metadata_update["risk_assessment_completed"] = True
    
    return {
        "risk_assessment": risk_assessment.model_dump(),
        "metadata": metadata_update,
        "execution_trace": [_record_trace("safety_monitor", start_time)]
    }
