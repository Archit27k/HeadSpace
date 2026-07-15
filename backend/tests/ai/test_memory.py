import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from app.ai.memory.manager import MemoryCoordinator
from app.ai.memory.retrieval import MemoryRanker, MemoryRetriever
from app.ai.memory.short_term import ShortTermMemory
from app.ai.memory.long_term import LongTermMemory
from app.ai.memory.summary import SummaryMemory
from app.ai.memory.semantic import SemanticMemory

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def memory_coordinator(mock_db):
    return MemoryCoordinator(db=mock_db)

def test_short_term_memory():
    stm = ShortTermMemory()
    user_id = uuid4()
    
    # Store
    res = stm.store(user_id, None, "test")
    assert res["status"] == "stored"
    
    # Retrieve
    state = {"messages": [{"role": "user", "content": "hi"} for _ in range(15)]}
    retrieved = stm.retrieve(user_id, None, state=state)
    
    assert len(retrieved) == 1
    assert retrieved[0]["type"] == "short_term"
    assert retrieved[0]["metadata"]["message_count"] == 10 # Should only extract last 10

def test_memory_ranker():
    ranker = MemoryRanker()
    memories = [
        {"type": "short_term", "relevance_score": 0.4},
        {"type": "long_term", "relevance_score": 0.9},
        {"type": "semantic", "relevance_score": 0.6}
    ]
    
    ranked = ranker.rank(memories)
    
    assert len(ranked) == 2 # 0.4 is below the 0.5 threshold
    assert ranked[0]["type"] == "long_term" # Highest score first
    assert ranked[1]["type"] == "semantic"

def test_memory_coordinator_retrieve(memory_coordinator):
    user_id = uuid4()
    session_id = uuid4()
    
    # Mocking retrieve methods internally
    memory_coordinator.short_term.retrieve = MagicMock(return_value=[{"type": "short_term", "relevance_score": 0.9}])
    memory_coordinator.long_term.retrieve = MagicMock(return_value=[{"type": "long_term", "relevance_score": 0.8}])
    memory_coordinator.summary.retrieve = MagicMock(return_value=[])
    memory_coordinator.semantic.retrieve = MagicMock(return_value=[])
    
    result = memory_coordinator.retrieve_context(user_id, session_id)
    
    assert "ranked_context" in result
    assert len(result["ranked_context"]) == 2
    assert result["metadata"]["total_retrieved"] == 2
    assert result["ranked_context"][0]["type"] == "short_term"

def test_memory_coordinator_store_compression(memory_coordinator):
    user_id = uuid4()
    session_id = uuid4()
    
    state = {"messages": [{"role": "user", "content": "hi"} for _ in range(25)]}
    
    # Track if store was called on summary
    memory_coordinator.summary.store = MagicMock()
    
    memory_coordinator.store_context(user_id, session_id, "general_chat", state)
    
    # With 25 messages, summary compression should be triggered
    memory_coordinator.summary.store.assert_called_once()
