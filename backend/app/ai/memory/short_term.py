from app.ai.memory.base import BaseMemory
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class ShortTermMemory(BaseMemory):
    """
    Handles thread-scoped conversation history and context.
    Typically interacts directly with the LangGraph state.
    """
    def __init__(self):
        # We don't maintain internal state here as LangGraph state is passed in via kwargs
        pass

    def store(self, user_id: UUID, session_id: Optional[UUID], data: Any, **kwargs) -> Any:
        logger.info(f"Storing short term memory for user {user_id}")
        return {"status": "stored", "type": "short_term", "data": data}

    def retrieve(self, user_id: UUID, session_id: Optional[UUID], query: str = None, **kwargs) -> List[Dict[str, Any]]:
        logger.info(f"Retrieving short term memory for user {user_id}")
        # In a real scenario, this extracts messages from the LangGraph state passed in kwargs
        state = kwargs.get("state", {})
        messages = state.get("messages", [])
        
        # Simple extraction of the last N messages for immediate context
        recent_messages = messages[-10:] if len(messages) > 10 else messages
        
        return [
            {
                "type": "short_term",
                "content": f"Recent interaction context: {len(recent_messages)} messages.",
                "relevance_score": 1.0,
                "metadata": {"message_count": len(recent_messages)}
            }
        ]

    def update(self, memory_id: UUID, data: Any, **kwargs) -> Any:
        # State updates in LangGraph are handled natively by the graph framework
        pass

    def delete(self, memory_id: UUID, **kwargs) -> bool:
        pass
