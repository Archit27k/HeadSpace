from pydantic import BaseModel
from typing import Type, Any, Dict, List
import abc

class BaseTool(abc.ABC):
    """
    Abstract base class for all tools in the LangGraph Tool Ecosystem.
    Provides schema validation, metadata, and execution interfaces.
    """
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    required_permissions: List[str] = []
    timeout_seconds: int = 10
    retry_policy: Dict[str, Any] = {"max_retries": 1, "backoff": 2}
    
    # Pydantic schemas for validation
    input_schema: Type[BaseModel]
    output_schema: Type[BaseModel]

    def validate_input(self, kwargs: Dict[str, Any]) -> BaseModel:
        """Validates incoming arguments against the input_schema."""
        return self.input_schema(**kwargs)
        
    def validate_output(self, result: Any) -> BaseModel:
        """Validates the tool result against the output_schema."""
        if isinstance(result, dict):
            return self.output_schema(**result)
        return self.output_schema(data=result)

    @abc.abstractmethod
    def _run(self, **kwargs) -> Any:
        """Synchronous tool execution. Must be overridden."""
        pass

    @abc.abstractmethod
    async def _arun(self, **kwargs) -> Any:
        """Asynchronous tool execution. Must be overridden."""
        pass
