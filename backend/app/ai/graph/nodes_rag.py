import time
import logging
from typing import Dict, Any, List
from app.ai.graph.state import GraphState
from app.ai.retrieval.qdrant import QdrantVectorStore
from app.ai.retrieval.reranker import CrossEncoderReranker

logger = logging.getLogger(__name__)

# Instances can be cached globally or injected
vector_store = QdrantVectorStore()
reranker = CrossEncoderReranker()

def _record_trace(node_name: str, start_time: float) -> Dict[str, Any]:
    return {"node": node_name, "latency_ms": round((time.time() - start_time) * 1000, 2)}

def query_rewriter(state: GraphState) -> Dict[str, Any]:
    """
    Rewrites the user's latest message into an optimized search query.
    In a real implementation, this uses a fast LLM call.
    """
    start_time = time.time()
    
    # Very simple mock rewriting logic for now
    messages = state.get("messages", [])
    if not messages:
        return {"execution_trace": [_record_trace("query_rewriter", start_time)]}
        
    original_query = messages[-1].get("content", "")
    
    # E.g. "I'm stressed about exams" -> "exam stress management techniques"
    optimized_query = f"mental health {original_query}"
    
    metadata = state.get("metadata", {})
    metadata["optimized_query"] = optimized_query
    
    return {
        "metadata": metadata,
        "execution_trace": [_record_trace("query_rewriter", start_time)]
    }

def hybrid_retriever(state: GraphState) -> Dict[str, Any]:
    """
    Executes the dense + sparse search across Qdrant collections.
    """
    start_time = time.time()
    query = state.get("metadata", {}).get("optimized_query", "")
    
    if not query:
        return {"execution_trace": [_record_trace("hybrid_retriever", start_time)]}
        
    collections_to_search = ["cbt_documents", "mental_health_guides"]
    all_results = []
    
    for collection in collections_to_search:
        res = vector_store.hybrid_search(query, query_vector=[], collection_name=collection, top_k=5)
        all_results.extend(res)
        
    metadata = state.get("metadata", {})
    metadata["raw_retrieval_results"] = all_results
    
    return {
        "metadata": metadata,
        "execution_trace": [_record_trace("hybrid_retriever", start_time)]
    }

def context_validator(state: GraphState) -> Dict[str, Any]:
    """
    Reranks the candidates using Cross-Encoder and drops those below threshold.
    """
    start_time = time.time()
    query = state.get("metadata", {}).get("optimized_query", "")
    raw_results = state.get("metadata", {}).get("raw_retrieval_results", [])
    
    if not query or not raw_results:
        return {"execution_trace": [_record_trace("context_validator", start_time)]}
        
    # Rerank
    ranked = reranker.rerank(query, raw_results, top_k=3)
    
    # Filter by threshold (e.g., must be > 0)
    # Since it's mock, we just take the top ones
    valid_context = [doc for doc in ranked if doc.get("rerank_score", 0.0) >= -10.0]
    
    # Inject into memory payload
    memory_update = state.get("memory", {})
    context_items = []
    for doc in valid_context:
        context_items.append({
            "type": "retrieved_knowledge",
            "content": doc["content"],
            "metadata": doc.get("metadata", {})
        })
        
    if "ranked_context" not in memory_update:
        memory_update["ranked_context"] = []
    memory_update["ranked_context"].extend(context_items)
    
    return {
        "memory": memory_update,
        "execution_trace": [_record_trace("context_validator", start_time)]
    }

def citation_generator(state: GraphState) -> Dict[str, Any]:
    """
    Appends citations to the final LLM response if retrieved knowledge was used.
    """
    start_time = time.time()
    messages = state.get("messages", [])
    if state.get("metadata", {}).get("skip_llm_generation"):
        return {"execution_trace": [_record_trace("citation_generator_skipped", start_time)]}
        
    memory = state.get("memory", {})
    retrieved_items = [item for item in memory.get("ranked_context", []) if item["type"] == "retrieved_knowledge"]
    
    if not retrieved_items or not messages:
        return {"execution_trace": [_record_trace("citation_generator", start_time)]}
        
    # Append citation footer to the assistant's last message
    last_msg = messages[-1]
    if last_msg["role"] == "assistant":
        citations = []
        for i, item in enumerate(retrieved_items):
            source = item.get("metadata", {}).get("source", "Unknown Source")
            citations.append(f"[{i+1}] {source}")
            
        if citations:
            footer = "\n\nSources:\n" + "\n".join(citations)
            last_msg["content"] += footer
            
    return {
        "messages": messages,
        "execution_trace": [_record_trace("citation_generator", start_time)]
    }
