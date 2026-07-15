from app.ai.memory.short_term import ShortTermMemory
from app.ai.memory.long_term import LongTermMemory
from app.ai.memory.semantic import SemanticMemory
from app.ai.memory.summary import SummaryMemory
from app.ai.memory.retrieval import MemoryRanker, MemoryRetriever
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
import time

logger = logging.getLogger(__name__)

class MemoryCoordinator:
    """
    The central coordinator for the memory subsystem.
    Integrates with LangGraph to provide unified read/write access to all memory layers.
    """
    def __init__(self, db: Session):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(db)
        self.semantic = SemanticMemory()
        self.summary = SummaryMemory(db)
        self.ranker = MemoryRanker()
        self.retriever = MemoryRetriever(self.ranker)
        
    def retrieve_context(self, user_id: UUID, session_id: Optional[UUID], query: str = None, state: Dict[str, Any] = None) -> Dict[str, Any]:
        """Gathers and ranks relevant context from all available memory systems."""
        start_time = time.time()
        logger.info(f"MemoryCoordinator: Gathering context for user {user_id}")
        
        raw_memories = []
        
        # 1. Fetch from all sources
        short_memories = self.short_term.retrieve(user_id, session_id, query, state=state)
        long_memories = self.long_term.retrieve(user_id, session_id, query)
        semantic_memories = self.semantic.retrieve(user_id, session_id, query)
        summary_memories = self.summary.retrieve(user_id, session_id, query)
        
        raw_memories.extend(short_memories)
        raw_memories.extend(long_memories)
        raw_memories.extend(semantic_memories)
        raw_memories.extend(summary_memories)
        
        # 2. Rank and filter
        ranked_context = self.retriever.retrieve_and_rank(query, raw_memories)
        
        latency = round((time.time() - start_time) * 1000, 2)
        logger.info(f"MemoryCoordinator: Retrieved and ranked {len(ranked_context)} items in {latency}ms")
        
        return {
            "ranked_context": ranked_context,
            "metadata": {
                "total_retrieved": len(raw_memories),
                "total_kept": len(ranked_context),
                "latency_ms": latency
            }
        }
        
    def store_context(self, user_id: UUID, session_id: Optional[UUID], intent: str, current_state: Dict[str, Any]) -> None:
        """Distributes new information to the appropriate memory systems based on intent or rules."""
        logger.info(f"MemoryCoordinator: Evaluating state for storage. Intent: {intent}")
        
        # Short term doesn't need explicit storage since it's in LangGraph state, but we could trigger summary compression
        messages = current_state.get("messages", [])
        
        # If conversation gets too long, trigger a summary (Compression event)
        if len(messages) > 20: # Arbitrary threshold
            logger.info("MemoryCoordinator: Message threshold reached, triggering summary compression")
            summary_data = self.summary.generate_summary(messages)
            self.summary.store(user_id, session_id, summary_data)
            
        # If intent indicates user preference or goal, store in long-term memory
        if intent == "wellness_goal_setting":
            # Extract facts (would use LLM tool in reality)
            fact = {"category": "wellness_goals", "fact_text": "User wants to meditate daily", "relevance_score": 1.0}
            self.long_term.store(user_id, session_id, fact)
