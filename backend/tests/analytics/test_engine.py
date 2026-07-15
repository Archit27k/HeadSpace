import pytest
from app.analytics.engine import AnalyticsEngine, TrendAnalyzer, PatternDetector
from app.analytics.explainability import ExplainabilityEngine

def test_trend_analyzer():
    trends = TrendAnalyzer.generate_mock_trends(days=7)
    assert len(trends) == 14  # 7 for Stress, 7 for Mood
    assert trends[0].category in ["Stress", "Mood"]

def test_pattern_detector():
    insights = PatternDetector.detect_patterns("user_123")
    assert len(insights) > 0
    assert insights[0].confidence > 0.0

def test_explainability_engine():
    rec_data = {"title": "Try 5 minutes of mindful breathing"}
    report = ExplainabilityEngine.explain_recommendation(rec_data)
    
    assert report.recommendation_id == "Try 5 minutes of mindful breathing"
    assert len(report.evidence_used) > 0
    assert "journal_" in report.relevant_journals[0]

def test_dashboard_summary():
    summary = AnalyticsEngine.get_dashboard_summary("user_123")
    assert "trends" in summary
    assert "insights" in summary
    assert len(summary["trends"]) > 0
