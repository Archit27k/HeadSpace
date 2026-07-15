import pytest
from pydantic import BaseModel, ValidationError
from typing import Any
from app.ai.tools.base import BaseTool
from app.ai.tools.registry import ToolRegistry
from app.ai.tools.engine import ToolExecutionEngine

class MockInput(BaseModel):
    user_id: str

class MockOutput(BaseModel):
    name: str
    age: int

class MockProfileTool(BaseTool):
    name = "MockProfileTool"
    description = "Fetches user profile"
    input_schema = MockInput
    output_schema = MockOutput
    required_permissions = ["read:profile"]
    retry_policy = {"max_retries": 2, "backoff": 1}
    
    def _run(self, **kwargs) -> Any:
        pass
        
    async def _arun(self, **kwargs) -> Any:
        user_id = kwargs.get("user_id")
        if user_id == "fail_me":
            raise Exception("Mock network failure")
        return {"name": "Alice", "age": 30}

@pytest.fixture
def engine():
    registry = ToolRegistry()
    registry.register(MockProfileTool())
    return ToolExecutionEngine(registry)

@pytest.mark.asyncio
async def test_tool_successful_execution(engine):
    result = await engine.execute_tool("MockProfileTool", {"user_id": "123"}, {})
    assert result.get("status") == "success"
    assert result["result"]["name"] == "Alice"
    assert "latency_ms" in result

@pytest.mark.asyncio
async def test_tool_input_validation_failure(engine):
    # Missing required 'user_id'
    result = await engine.execute_tool("MockProfileTool", {}, {})
    assert "error" in result
    assert "Input validation failed" in result["error"]

@pytest.mark.asyncio
async def test_tool_retry_and_failure(engine):
    # Triggers the exception inside _arun
    result = await engine.execute_tool("MockProfileTool", {"user_id": "fail_me"}, {})
    assert "error" in result
    assert "Execution failed" in result["error"]
    assert "Mock network failure" in result["error"]

@pytest.mark.asyncio
async def test_tool_not_found(engine):
    result = await engine.execute_tool("NonExistentTool", {}, {})
    assert "error" in result
    assert "not found" in result["error"]
