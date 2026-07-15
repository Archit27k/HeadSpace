from typing import Dict, Any
from datetime import datetime
from app.analytics.engine import AnalyticsEngine

class ReportGenerator:
    """
    Generates weekly and monthly wellness reports.
    """
    
    @staticmethod
    def generate_weekly_report(user_id: str) -> Dict[str, Any]:
        """
        Generates a summary of the past 7 days.
        """
        summary = AnalyticsEngine.get_dashboard_summary(user_id)
        insights = summary.get("insights", [])
        
        return {
            "report_type": "Weekly",
            "generated_at": datetime.utcnow().isoformat(),
            "summary": "Your weekly wellness metrics have been compiled from your latest mood logs and journal entries.",
            "achievements": [f"Logged data on {summary.get('total_entries', 0)} instances this week."],
            "areas_of_focus": ["Review your latest insights" if insights else "Log more journals to get insights."],
            "insights": insights
        }
        
    @staticmethod
    def generate_monthly_report(user_id: str) -> Dict[str, Any]:
        """
        Generates a summary of the past 30 days.
        """
        summary = AnalyticsEngine.get_dashboard_summary(user_id)
        insights = summary.get("insights", [])
        
        return {
            "report_type": "Monthly",
            "generated_at": datetime.utcnow().isoformat(),
            "summary": "Your monthly wellness metrics have been compiled from your latest mood logs and journal entries.",
            "achievements": [f"Logged data on {summary.get('total_entries', 0)} instances this month."],
            "areas_of_focus": ["Review your latest insights" if insights else "Log more journals to get insights."],
            "insights": insights
        }
