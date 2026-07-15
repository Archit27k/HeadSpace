from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from uuid import UUID

class BaseMemory(ABC):
    """Abstract base class for all memory systems."""
    
    @abstractmethod
    def store(self, user_id: UUID, session_id: Optional[UUID], data: Any, **kwargs) -> Any:
        """Stores new memory information."""
        pass
        
    @abstractmethod
    def retrieve(self, user_id: UUID, session_id: Optional[UUID], query: str = None, **kwargs) -> List[Dict[str, Any]]:
        """Retrieves relevant memory context."""
        pass
        
    @abstractmethod
    def update(self, memory_id: UUID, data: Any, **kwargs) -> Any:
        """Updates an existing memory item."""
        pass
        
    @abstractmethod
    def delete(self, memory_id: UUID, **kwargs) -> bool:
        """Deletes a memory item."""
        pass
