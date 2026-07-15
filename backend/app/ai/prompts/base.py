from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class BasePromptTemplate(ABC):
    """
    Abstract base class for all prompt templates.
    Enforces a strict structure for prompt definitions, ensuring all 
    prompts have versioning, required variables, and optional schemas.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for the prompt template."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this prompt is used for."""
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        """Semantic version of the prompt (e.g., '1.0.0')."""
        pass
        
    @property
    @abstractmethod
    def input_variables(self) -> List[str]:
        """List of variable keys required to render the prompt."""
        pass
        
    @property
    def output_schema(self) -> Optional[type[BaseModel]]:
        """Optional Pydantic model dictating the expected structured output."""
        return None
        
    @abstractmethod
    def render(self, **kwargs) -> str:
        """
        Renders the final prompt string.
        Should raise ValueError if required input_variables are missing.
        """
        pass
