import pytest
from unittest.mock import patch
from app.analytics.engine import AnalyticsEngine, TrendAnalyzer, PatternDetector
from app.analytics.explainability import ExplainabilityEngine
from app.schemas.analytics import TrendData, Insight

@patch("app.analytics.engine.TrendAnalyzer.get_real_trends")
def test_trend_analyzer(mock_get_real_trends):
    mock_get_real_trends.return_value = [
        TrendData(date="2023-01-01", score=5.0, category="Mood"),
        TrendData(date="2023-01-01", score=3.0, category="Stress")
    ]
    trends = TrendAnalyzer.get_real_trends("user_123", days=7)
    assert len(trends) == 2
    assert trends[0].category in ["Stress", "Mood"]

@patch("app.analytics.engine.PatternDetector.detect_patterns")
def test_pattern_detector(mock_detect_patterns):
    mock_detect_patterns.return_value = [
        Insight(title="Mock Insight", description="test", confidence=0.8, insight_type="Behavior Pattern")
    ]
    insights = PatternDetector.detect_patterns("user_123")
    assert len(insights) > 0
    assert insights[0].confidence > 0.0

def test_explainability_engine():
    rec_data = {"title": "Try 5 minutes of mindful breathing"}
    report = ExplainabilityEngine.explain_recommendation(rec_data)
    
    assert report.recommendation_id == "Try 5 minutes of mindful breathing"
    assert len(report.evidence_used) > 0
    assert "journal_" in report.relevant_journals[0]

@patch("app.analytics.engine.TrendAnalyzer.get_real_trends")
@patch("app.analytics.engine.PatternDetector.detect_patterns")
def test_dashboard_summary(mock_detect, mock_trends):
    mock_trends.return_value = [TrendData(date="2023-01-01", score=5.0, category="Mood")]
    mock_detect.return_value = [Insight(title="Mock Insight", description="test", confidence=0.8, insight_type="Behavior Pattern")]
    summary = AnalyticsEngine.get_dashboard_summary("user_123")
    assert "trends" in summary
    assert "insights" in summary
    assert len(summary["trends"]) > 0
