import pytest
from app.ai.graph.builder import build_orchestration_graph
from app.ai.graph.state import GraphState

@pytest.mark.asyncio
async def test_graph_execution():
    """Tests the full orchestration layer graph from start to end."""
    graph = build_orchestration_graph()
    
    # Initialize state
    initial_state = {
        "conversation_id": "test_conv_123",
        "user_id": "test_user_456",
        "messages": [{"role": "user", "content": "Just writing a test journal entry."}],
        "current_intent": None,
        "emotion": {},
        "retrieved_context": [],
        "planner_decisions": {},
        "memory": {},
        "tool_outputs": [],
        "validation_results": {},
        "metadata": {},
        "execution_trace": []
    }
    
    # Execute the graph
    result = await graph.ainvoke(initial_state)
    
    # Verify the trace ran through all the major expected nodes sequentially based on our routing
    # Expected Nodes: 
    # conversation_entry -> intent_detection -> planner -> memory_manager -> emotion_service
    # -> retriever -> prompt_builder -> llm_provider -> response_validator -> persistence -> response_node
    
    traces = result.get("execution_trace", [])
    
    # There should be 11 execution trace elements corresponding to our 11 nodes.
    # Note: In an actual LangGraph with sub-graphs or complex conditional logic, this list might be longer/shorter,
    # but based on our sequential logic defined in builder.py, we expect exactly 11.
    assert len(traces) == 11
    
    node_names = [trace["node"] for trace in traces]
    
    assert "conversation_entry" in node_names
    assert "planner" in node_names
    assert "emotion_service" in node_names
    assert "llm_provider" in node_names
    assert "persistence" in node_names
    
    # Specific assertions based on our mock implementations
    assert result["metadata"]["status"] == "initialized"
    assert result["current_intent"] == "journal_entry"  # Intent detection should trigger on 'journal'
    assert result["planner_decisions"]["use_tools"] is True
    assert result["metadata"]["persisted"] is True
    
    # LLM should have appended a message
    assert len(result["messages"]) == 2
    assert result["messages"][1]["role"] == "assistant"
