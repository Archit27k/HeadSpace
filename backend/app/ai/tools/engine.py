import time
import logging
from typing import Dict, Any, List
from pydantic import ValidationError
from app.ai.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)

class ToolExecutionEngine:
    """
    Safely executes tools from the registry.
    Handles permissions, retries, validation, and execution tracing.
    """
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def _check_permissions(self, required_perms: List[str], user_context: Dict[str, Any]) -> bool:
        """Mock permission validation."""
        # In a real environment, check user_context against required_perms
        return True

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a tool by name with provided arguments."""
        start_time = time.time()
        tool = self.registry.get_tool(tool_name)
        
        if not tool:
            return {"error": f"Tool '{tool_name}' not found."}
            
        if not self._check_permissions(tool.required_permissions, user_context):
            return {"error": "Permission denied for this tool."}
            
        try:
            # 1. Validate Input Schema
            validated_input = tool.validate_input(arguments)
        except ValidationError as e:
            return {"error": f"Input validation failed: {e.errors()}"}
            
        # 2. Execution with basic retry/timeout handling (mocked retry via a simple loop for now)
        # Note: In production, we'd use tenacity.retry decorators dynamically based on tool.retry_policy
        max_retries = tool.retry_policy.get("max_retries", 1)
        result_data = None
        error_msg = None
        
        for attempt in range(max_retries):
            try:
                # Async execution
                result_data = await tool._arun(**validated_input.model_dump())
                break
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Tool {tool_name} failed attempt {attempt + 1}: {e}")
                
        if result_data is None and error_msg is not None:
            return {"error": f"Execution failed after {max_retries} attempts: {error_msg}"}
            
        try:
            # 3. Validate Output Schema
            validated_output = tool.validate_output(result_data)
        except ValidationError as e:
            return {"error": f"Output validation failed: {e.errors()}"}
            
        latency = (time.time() - start_time) * 1000
        logger.info(f"Tool {tool_name} executed successfully in {latency:.2f}ms")
        
        return {
            "tool": tool_name,
            "status": "success",
            "result": validated_output.model_dump(),
            "latency_ms": latency
        }
