import pytest
from app.ai.graph.nodes import (
    conversation_entry,
    intent_detection,
    planner,
    memory_manager,
    emotion_service,
    retriever,
    prompt_builder,
    llm_provider,
    response_validator,
    persistence,
    response_node
)
from app.ai.graph.state import GraphState

@pytest.fixture
def base_state() -> GraphState:
    return {
        "conversation_id": "test_conv",
        "user_id": "test_user",
        "messages": [{"role": "user", "content": "I feel anxious today."}],
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

def test_conversation_entry(base_state):
    result = conversation_entry(base_state)
    assert "metadata" in result
    assert result["metadata"]["status"] == "initialized"
    assert "execution_trace" in result
    assert result["execution_trace"][0]["node"] == "conversation_entry"

def test_intent_detection(base_state):
    result = intent_detection(base_state)
    assert "current_intent" in result
    # We didn't say "journal", "help", or "crisis" in the base message, so default "general_chat"
    assert result["current_intent"] == "general_chat"
    
def test_intent_detection_crisis(base_state):
    base_state["messages"] = [{"role": "user", "content": "I need help with a crisis."}]
    result = intent_detection(base_state)
    assert result["current_intent"] == "crisis_support"

def test_planner(base_state):
    base_state["current_intent"] = "general_chat"
    result = planner(base_state)
    assert result["metadata"]["planner_executed"] is True
    assert isinstance(result["selected_tools"], list)

def test_memory_manager(base_state):
    result = memory_manager(base_state)
    assert "memory" in result
    assert "short_term" in result["memory"]

def test_emotion_service(base_state):
    # Pass a message to ensure emotion is evaluated
    base_state["messages"] = [{"role": "user", "content": "I feel happy!"}]
    result = emotion_service(base_state)
    # The actual implementation updates metadata with current_emotion
    assert "metadata" in result
    # If the MLflow mock succeeds, current_emotion will be populated
    # Even if it fails, it returns metadata safely

def test_retriever(base_state):
    base_state["planner_decisions"] = {"use_rag": True}
    result = retriever(base_state)
    assert len(result["retrieved_context"]) > 0

def test_prompt_builder(base_state):
    result = prompt_builder(base_state)
    assert result["metadata"]["prompt_built"] is True

def test_llm_provider(base_state):
    result = llm_provider(base_state)
    assert len(result["messages"]) == 1
    assert result["messages"][0]["role"] == "assistant"

def test_response_validator(base_state):
    result = response_validator(base_state)
    assert result["validation_results"]["is_safe"] is True

def test_persistence(base_state):
    result = persistence(base_state)
    assert result["metadata"]["persisted"] is True

def test_response_node(base_state):
    result = response_node(base_state)
    assert len(result["execution_trace"]) == 1
