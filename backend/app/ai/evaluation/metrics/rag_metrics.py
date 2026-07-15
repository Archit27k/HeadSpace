import logging

logger = logging.getLogger(__name__)

class RagMetrics:
    """
    Wraps the 'ragas' library to evaluate RAG pipelines.
    (Mocked for this implementation to avoid heavy LLM dependency during CI).
    """
    
    @staticmethod
    def evaluate(question: str, answer: str, contexts: list[str]) -> dict:
        """
        In a full implementation, this would use ragas metrics like 
        Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall.
        """
        logger.info(f"Evaluating RAG for question: {question}")
        
        try:
            # We try to import to see if ragas is installed
            import ragas
        except ImportError:
            pass
            
        # Mock evaluation for demonstration
        faithfulness_score = 0.9 if answer else 0.0
        context_precision = 0.85 if contexts else 0.0
        
        return {
            "faithfulness": faithfulness_score,
            "context_precision": context_precision,
            "answer_relevance": 0.9,
            "context_recall": 0.8
        }
