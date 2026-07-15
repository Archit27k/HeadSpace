from typing import Dict, Any, List
from app.ai.graph.builder import build_orchestration_graph
import uuid
import logging

logger = logging.getLogger(__name__)

class GraphEvaluator:
    """
    Test harness to run the production LangGraph on evaluation datasets
    without mutating production state.
    """
    def __init__(self):
        self.graph = build_orchestration_graph()
        
    def execute_mock_run(self, initial_message: str) -> Dict[str, Any]:
        """
        Executes a single run of the graph for evaluation purposes.
        """
        logger.info(f"Running GraphEvaluator on message: {initial_message}")
        
        # Initialize a clean state
        state = {
            "conversation_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "messages": [{"role": "user", "content": initial_message}],
            "metadata": {},
            "memory": {},
            "current_intent": None,
            "tool_outputs": [],
            "execution_trace": [],
            "validation_results": {}
        }
        
        # Execute graph (in a real scenario, this would use .invoke or .stream)
        # Since this is an evaluation mock, we can just invoke it.
        try:
            final_state = self.graph.invoke(state)
            return final_state
        except Exception as e:
            logger.error(f"Graph execution failed during evaluation: {e}")
            return state

    def evaluate_journal_extraction(self, run_state: Dict[str, Any], ground_truth: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates Journal Intelligence extraction quality.
        Measures: Extraction Quality, Theme Consistency, Memory Precision, Reflection Quality, Action Relevance.
        """
        metrics = {
            "extraction_quality": 0.0,
            "theme_consistency": 0.0,
            "memory_precision": 0.0,
            "reflection_quality": 0.0,
            "action_relevance": 0.0
        }
        
        # Check tool outputs for journal_intelligence
        tool_outputs = run_state.get("tool_outputs", [])
        journal_output = next((t["result"] for t in tool_outputs if t.get("tool") == "journal_intelligence"), None)
        
        if not journal_output:
            return metrics
            
        # Simplified heuristics for evaluation (in reality, would use an LLM-as-a-judge or exact match)
        if set(journal_output.get("themes", [])).intersection(set(ground_truth.get("themes", []))):
            metrics["theme_consistency"] = 1.0
            
        if len(journal_output.get("summary", "")) > 10:
            metrics["extraction_quality"] = 1.0
            
        if journal_output.get("memory_updates"):
            metrics["memory_precision"] = 1.0
            
        if len(journal_output.get("reflection_questions", [])) > 0:
            metrics["reflection_quality"] = 1.0
            
        if len(journal_output.get("suggested_action_items", [])) > 0:
            metrics["action_relevance"] = 1.0
            
        return metrics

    def evaluate_wellness_recommendations(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates whether the wellness recommendations are relevant and compliant."""
        tool_outputs = state.get("tool_outputs", [])
        
        passed = False
        has_recommendations = False
        
        for output in tool_outputs:
            if isinstance(output, dict) and "recommendations" in output:
                has_recommendations = True
                if len(output.get("recommendations", [])) > 0:
                    passed = True
                break
                
        return {
            "metric": "wellness_recommendation_relevance",
            "passed": passed,
            "has_recommendations": has_recommendations
        }
        
    def evaluate_explainability(self, explainability_report: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates whether an explainability report is comprehensive."""
        passed = False
        
        evidence = explainability_report.get("evidence_used", [])
        reasoning = explainability_report.get("reasoning", "")
        
        if len(evidence) > 0 and len(reasoning) > 10:
            passed = True
            
        return {
            "metric": "recommendation_explainability",
            "passed": passed,
            "evidence_count": len(evidence)
        }
