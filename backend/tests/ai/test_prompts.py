import pytest
from app.ai.prompts.registry import prompt_registry, PromptRegistry
from app.ai.prompts.templates.system import SystemChatPrompt
from app.ai.prompts.builder import ContextBuilder, PromptBuilder

def test_registry_registration():
    registry = PromptRegistry()
    template = SystemChatPrompt()
    registry.register(template)
    
    fetched = registry.get("system_chat")
    assert fetched.version == "1.0.0"
    
def test_system_prompt_rendering():
    template = SystemChatPrompt()
    
    # Missing variable should raise ValueError
    with pytest.raises(ValueError):
        template.render(user_name="Alice")
        
    # Valid render
    output = template.render(user_name="Alice", context_str="Some context", rules="Be nice")
    assert "Alice" in output
    assert "Some context" in output
    assert "Be nice" in output

def test_context_builder():
    memories = [
        {"type": "short_term", "content": "Hello"}
    ]
    
    result = ContextBuilder.build_context_string(memories)
    assert "[SHORT_TERM]: Hello" in result
    
    rules = ContextBuilder.get_system_rules("crisis_support")
    assert "IMMEDIATE RULE" in rules

def test_prompt_builder():
    prompt_registry.register(SystemChatPrompt())
    
    state = {
        "memory": {"ranked_context": [{"type": "info", "content": "test"}]},
        "current_intent": "general_chat"
    }
    user = {"first_name": "Bob"}
    
    result = PromptBuilder.build_system_prompt("system_chat", state, user)
    
    assert "Bob" in result
    assert "test" in result
    assert "empathetic" in result # from default rules
