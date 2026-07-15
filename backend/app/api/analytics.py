from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.models.models import User
from app.analytics.engine import AnalyticsEngine
from app.analytics.reports import ReportGenerator
from app.analytics.explainability import ExplainabilityEngine
from app.schemas.analytics import DashboardSummary, ExplainabilityReport
from typing import Dict, Any

router = APIRouter()

@router.get("/dashboard", response_model=DashboardSummary)
async def get_analytics_dashboard(current_user: User = Depends(get_current_user)):
    """Returns the main analytics dashboard summary (trends and insights)."""
    summary = AnalyticsEngine.get_dashboard_summary(str(current_user.id))
    return DashboardSummary(**summary)

@router.get("/reports/weekly")
async def get_weekly_report(current_user: User = Depends(get_current_user)):
    """Returns the generated weekly report."""
    return ReportGenerator.generate_weekly_report(str(current_user.id))

@router.post("/explain", response_model=ExplainabilityReport)
async def explain_recommendation(recommendation_data: Dict[str, Any], current_user: User = Depends(get_current_user)):
    """Returns the explainability report for a given recommendation."""
    try:
        report = ExplainabilityEngine.explain_recommendation(recommendation_data)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
