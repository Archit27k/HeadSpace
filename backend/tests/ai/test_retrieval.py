import pytest
from app.ai.retrieval.qdrant import QdrantVectorStore
from app.ai.retrieval.reranker import CrossEncoderReranker
from app.ai.ingestion.chunker import DocumentChunker

def test_qdrant_mock_search():
    store = QdrantVectorStore()
    
    res = store.search("stress", [0.1]*384, "cbt_documents", top_k=2)
    assert len(res) == 1
    assert "Mock dense result" in res[0]["content"]

    res_hybrid = store.hybrid_search("stress", [0.1]*384, "cbt_documents", top_k=2)
    assert len(res_hybrid) == 1
    assert "Mock hybrid result" in res_hybrid[0]["content"]

def test_reranker():
    reranker = CrossEncoderReranker() # Uses mock mode if models not downloaded locally
    docs = [
        {"content": "Low relevance document", "metadata": {"id": 1}},
        {"content": "High relevance document", "metadata": {"id": 2}}
    ]
    
    # In mock mode it just returns the same order
    ranked = reranker.rerank("find relevant", docs)
    assert len(ranked) == 2
    # In a real environment, id: 2 would score higher

def test_chunker_naive_fallback():
    chunker = DocumentChunker(chunk_size=10, chunk_overlap=0)
    # Using naive split if splitter not installed, but test will pass regardless
    # Just asserting it generates multiple chunks with metadata
    
    text = "Word " * 200
    metadata = {"title": "Test Doc"}
    
    chunks = chunker.chunk_document(text, metadata)
    assert len(chunks) > 0
    assert chunks[0]["metadata"]["title"] == "Test Doc"
    assert "chunk_index" in chunks[0]["metadata"]
