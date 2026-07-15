from typing import List, Dict, Any
from app.schemas.analytics import TrendData, Insight
from datetime import datetime, timedelta
import random

class TrendAnalyzer:
    @staticmethod
    def get_real_trends(user_id: str, days: int = 14) -> List[TrendData]:
        from app.models.database import SessionLocal
        from app.models.models import MoodLog, EmotionTimelineItem
        import uuid
        
        trends = []
        try:
            db = SessionLocal()
            uid = uuid.UUID(user_id)
            cutoff = datetime.utcnow() - timedelta(days=days)
            
            # Get MoodLogs
            moods = db.query(MoodLog).filter(MoodLog.user_id == uid, MoodLog.created_at >= cutoff).all()
            for m in moods:
                trends.append(TrendData(
                    date=m.created_at.strftime("%Y-%m-%d"),
                    score=float(m.score),
                    category="Mood"
                ))
                
            # Get EmotionTimelineItem (Risk score as stress proxy)
            emotions = db.query(EmotionTimelineItem).filter(EmotionTimelineItem.user_id == uid, EmotionTimelineItem.created_at >= cutoff).all()
            for e in emotions:
                # Map risk score (0-1) to 1-10 stress score
                stress = (float(e.risk_score) * 9) + 1
                trends.append(TrendData(
                    date=e.created_at.strftime("%Y-%m-%d"),
                    score=round(stress, 1),
                    category="Stress"
                ))
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Error fetching trends: {e}")
        finally:
            if 'db' in locals():
                db.close()
                
        return trends

class PatternDetector:
    @staticmethod
    def detect_patterns(user_id: str) -> List[Insight]:
        """Detects recurring patterns in user behavior and journals."""
        # We can implement real detection here later, for now we will query memory items labeled as insights.
        from app.models.database import SessionLocal
        from app.models.models import LongTermMemoryItem
        import uuid
        insights = []
        try:
            db = SessionLocal()
            uid = uuid.UUID(user_id)
            memories = db.query(LongTermMemoryItem).filter(LongTermMemoryItem.user_id == uid, LongTermMemoryItem.category == "Pattern").limit(5).all()
            for m in memories:
                insights.append(Insight(
                    title="Detected Pattern",
                    description=m.content,
                    confidence=float(m.importance_score),
                    insight_type="Behavior Pattern"
                ))
        except Exception:
            pass
        finally:
            if 'db' in locals():
                db.close()
        return insights

class AnalyticsEngine:
    @staticmethod
    def get_dashboard_summary(user_id: str) -> Dict[str, Any]:
        """Aggregates all analytics data for the dashboard."""
        trends = TrendAnalyzer.get_real_trends(user_id)
        insights = PatternDetector.detect_patterns(user_id)
        
        # Calculate summary metrics
        mood_scores = [t.score for t in trends if t.category == "Mood"]
        average_mood = round(sum(mood_scores)/len(mood_scores), 1) if mood_scores else None
        
        return {
            "average_mood": average_mood,
            "total_entries": len(trends),
            "active_days": len(set(t.date for t in trends)),
            "trends": [t.model_dump() for t in trends],
            "insights": [i.model_dump() for i in insights],
            "recent_explanations": []
        }
