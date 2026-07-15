from typing import TypedDict, List, Dict, Any, Optional, Annotated
import operator

# State for the LangGraph Orchestration Layer
class GraphState(TypedDict):
    # Core Identity
    conversation_id: str
    user_id: str
    
    # Message History
    # Annotated with operator.add means new messages are appended instead of replacing the list
    messages: Annotated[List[Dict[str, Any]], operator.add]
    
    # AI Understanding
    current_intent: Optional[str]
    emotion: Dict[str, Any]
    risk_assessment: Optional[Dict[str, Any]]
    
    # RAG / Context
    retrieved_context: List[Dict[str, Any]]
    
    # Execution & Routing
    planner_decisions: Dict[str, Any]
    
    # Memory Systems
    memory: Dict[str, Any]
    
    # Tool Execution
    selected_tools: List[Dict[str, Any]]
    tool_outputs: Annotated[List[Dict[str, Any]], operator.add]
    
    # Quality & Validation
    validation_results: Dict[str, Any]
    
    # Observability
    metadata: Dict[str, Any]
    execution_trace: Annotated[List[Dict[str, Any]], operator.add]
