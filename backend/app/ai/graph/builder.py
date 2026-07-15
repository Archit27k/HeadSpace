from langgraph.graph import StateGraph, END
from app.ai.graph.state import GraphState
from app.ai.graph import nodes, nodes_rag

def build_orchestration_graph() -> StateGraph:
    """
    Constructs the LangGraph orchestration layer.
    """
    workflow = StateGraph(GraphState)
    
    # 1. Add Core Nodes
    workflow.add_node("conversation_entry", nodes.conversation_entry)
    workflow.add_node("intent_detection", nodes.intent_detection)
    workflow.add_node("planner", nodes.planner)
    workflow.add_node("memory_manager", nodes.memory_manager)
    workflow.add_node("emotion_service", nodes.emotion_service)
    
    # 1b. Add Agentic RAG Nodes
    workflow.add_node("query_rewriter", nodes_rag.query_rewriter)
    workflow.add_node("hybrid_retriever", nodes_rag.hybrid_retriever)
    workflow.add_node("context_validator", nodes_rag.context_validator)
    
    # 1c. Add Generation Nodes
    workflow.add_node("prompt_builder", nodes.prompt_builder)
    workflow.add_node("llm_provider", nodes.llm_provider)
    workflow.add_node("response_validator", nodes.response_validator)
    workflow.add_node("citation_generator", nodes_rag.citation_generator)
    workflow.add_node("persistence", nodes.persistence)
    workflow.add_node("response_node", nodes.response_node)
    
    # 2. Define Routing Logic
    workflow.set_entry_point("conversation_entry")
    workflow.add_edge("conversation_entry", "intent_detection")
    
    from app.ai.graph import nodes_safety
    workflow.add_node("safety_monitor", nodes_safety.safety_monitor)
    
    # Emotion before safety_monitor, safety_monitor before planner
    workflow.add_edge("intent_detection", "emotion_service")
    workflow.add_edge("emotion_service", "safety_monitor")
    workflow.add_edge("safety_monitor", "planner")
    
    # Tool Execution
    workflow.add_node("tool_execution", nodes.tool_execution)
    workflow.add_edge("planner", "tool_execution")
    
    # Memory
    workflow.add_edge("tool_execution", "memory_manager")
    
    # Conditional RAG (assuming planner always says yes for now)
    workflow.add_edge("memory_manager", "query_rewriter")
    workflow.add_edge("query_rewriter", "hybrid_retriever")
    workflow.add_edge("hybrid_retriever", "context_validator")
    workflow.add_edge("context_validator", "prompt_builder")
    
    # Synthesis & Generation
    workflow.add_edge("prompt_builder", "llm_provider")
    workflow.add_edge("llm_provider", "response_validator")
    workflow.add_edge("response_validator", "citation_generator")
    
    # Persistence & End
    workflow.add_edge("citation_generator", "persistence")
    workflow.add_edge("persistence", "response_node")
    workflow.add_edge("response_node", END)
    
    return workflow.compile()
