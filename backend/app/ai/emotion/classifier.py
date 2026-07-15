import time
import logging
from datetime import datetime
from typing import Dict, Any, List
from app.ai.emotion.schemas import EmotionResult

logger = logging.getLogger(__name__)

class MLflowEmotionService:
    """
    Integrates with MLflow Model Registry to load the Champion classifier
    and run emotion inference on user messages.
    """
    def __init__(self, model_uri: str = "models:/EmotionClassifier/Champion"):
        self.model_uri = model_uri
        self.model = None
        self.version = "1.0.0 (Mock)" # Fallback version
        
        try:
            import mlflow
            # In a real environment with MLflow tracking server running:
            # self.model = mlflow.pyfunc.load_model(model_uri=self.model_uri)
            # self.version = "mlflow-champion"
            logger.info(f"Initialized MLflowEmotionService with URI: {self.model_uri}")
        except ImportError:
            logger.warning("mlflow not installed. EmotionService running in Mock Mode.")

    def _calculate_risk(self, primary_emotion: str, confidence: float) -> float:
        """
        Calculates a clinical risk score based on the emotion and confidence.
        """
        high_risk = ["anger", "sadness", "fear", "anxiety"]
        medium_risk = ["confusion", "frustration"]
        
        if primary_emotion in high_risk:
            # E.g., high confidence sadness = high risk
            return min(1.0, 0.4 + (confidence * 0.6))
        elif primary_emotion in medium_risk:
            return 0.3 * confidence
        return 0.0

    def predict(self, text: str) -> EmotionResult:
        """
        Runs inference and returns a structured EmotionResult.
        """
        start_time = time.time()
        
        # Mock prediction logic if model is not actually loaded via MLflow
        if not self.model:
            logger.info("Running mock emotion prediction")
            # Very simple mock routing based on keywords
            text_lower = text.lower()
            if any(w in text_lower for w in ["kill", "die", "terrible", "hopeless"]):
                primary = "sadness"
                dist = {"sadness": 0.9, "fear": 0.05, "anger": 0.05}
            elif any(w in text_lower for w in ["angry", "mad", "hate"]):
                primary = "anger"
                dist = {"anger": 0.85, "frustration": 0.1, "sadness": 0.05}
            else:
                primary = "joy"
                dist = {"joy": 0.7, "neutral": 0.2, "surprise": 0.1}
                
            confidence = dist[primary]
        else:
            # Real MLflow inference
            # df = pd.DataFrame({"text": [text]})
            # preds = self.model.predict(df)
            # ... process real predictions ...
            pass
            
        risk = self._calculate_risk(primary, confidence)
        inference_time = (time.time() - start_time) * 1000
        
        return EmotionResult(
            primary_emotion=primary,
            secondary_emotions=[k for k, v in dist.items() if k != primary and v > 0.1],
            confidence=confidence,
            emotion_distribution=dist,
            risk_score=risk,
            requires_follow_up=risk > 0.7,
            model_version=self.version,
            inference_time_ms=inference_time,
            timestamp=datetime.utcnow()
        )
