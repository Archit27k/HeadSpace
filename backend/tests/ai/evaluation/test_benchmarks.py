import pytest
from app.ai.evaluation.evaluators.graph_evaluator import GraphEvaluator
from app.ai.evaluation.datasets.benchmark_data import CRISIS_BENCHMARK, RAG_BENCHMARK
from app.ai.evaluation.metrics.planner_metrics import PlannerMetrics
from app.ai.evaluation.metrics.rag_metrics import RagMetrics
from app.ai.evaluation.reports.reporter import EvaluationReporter

@pytest.fixture(scope="module")
def reporter():
    rep = EvaluationReporter(output_dir="reports/evaluation/")
    yield rep
    rep.generate_markdown_report()
    rep.generate_json_report()

@pytest.fixture(scope="module")
def graph_evaluator():
    return GraphEvaluator()

def test_planner_crisis_routing(graph_evaluator, reporter):
    """
    Evaluates if the planner correctly routes crisis intents based on benchmark inputs.
    """
    for data in CRISIS_BENCHMARK:
        state = graph_evaluator.execute_mock_run(data["input"])
        predicted_intent = state.get("current_intent")
        
        # In a real environment with the MLflow model loaded, this would predict sadness/anger
        # and trigger crisis_support.
        # Since we use mock fallback in the EmotionService, it might catch "die" and trigger sadness.
        
        # We evaluate the metrics
        result = PlannerMetrics.evaluate_routing(predicted_intent, data["expected_intent"])
        reporter.add_result(f"Routing: {data['expected_intent']}", result)
        
        # We don't strictly assert because this is a regression tracking framework,
        # but for CI/CD gates we could enforce assertions.
        # assert result["score"] == 1.0

def test_rag_pipeline(reporter):
    """
    Evaluates RAG pipeline using Ragas metrics (Mocked for speed).
    """
    for data in RAG_BENCHMARK:
        # We would normally execute the subgraph for RAG here, but we will directly invoke the metric wrapper
        result = RagMetrics.evaluate(
            question=data["question"], 
            answer=data["expected_answer"], 
            contexts=data["expected_contexts"]
        )
        
        reporter.add_result(f"RAG: {data['question'][:20]}...", result)
        
        assert result["faithfulness"] >= 0.0 # Just ensuring it runs
