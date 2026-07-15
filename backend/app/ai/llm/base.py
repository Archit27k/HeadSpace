from abc import ABC, abstractmethod
from typing import Dict, Any, List, Generator

class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""
    
    @abstractmethod
    def generate(self, prompt: str, system_message: str = None) -> str:
        """Generates a text response."""
        pass
        
    @abstractmethod
    def generate_chat(self, messages: List[Dict[str, str]], system_message: str = None) -> str:
        """Generates a text response given a chat history."""
        pass
        
    @abstractmethod
    def generate_stream(self, messages: List[Dict[str, str]], system_message: str = None) -> Generator[str, None, None]:
        """Generates a streaming response given a chat history."""
        pass
        
    @abstractmethod
    def generate_structured(self, messages: List[Dict[str, str]], schema: Any, system_message: str = None) -> Dict[str, Any]:
        """Generates a structured JSON response matching the provided schema."""
        pass
