from typing import Dict, Any
from app.schemas.analytics import ExplainabilityReport

class ExplainabilityEngine:
    """
    Provides transparent reasoning for generated recommendations.
    """
    
    @staticmethod
    def explain_recommendation(recommendation_data: Dict[str, Any]) -> ExplainabilityReport:
        """
        Maps a recommendation to the underlying evidence (journals, memory, emotions) that generated it.
        """
        # In a real system, we'd look up the recommendation ID and its generation context.
        # Here we mock the mapping for the dashboard.
        rec_title = recommendation_data.get("title", "Unknown Recommendation")
        
        return ExplainabilityReport(
            recommendation_id=rec_title,
            evidence_used=[
                "High stress detected in last 3 journal entries",
                "User goal: 'Improve sleep quality' (Memory)",
                "Emotion Risk Level: Moderate (Graph State)"
            ],
            relevant_journals=["journal_102", "journal_104"],
            confidence=0.88,
            reasoning=f"The recommendation '{rec_title}' was generated because your recent entries indicate elevated stress affecting your sleep goals."
        )
