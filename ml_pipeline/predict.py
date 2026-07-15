import mlflow
import os
import numpy as np
from .config import config
from .preprocessing import clean_text
from .embedding_generator import EmbeddingGenerator

class EmotionPredictor:
    def __init__(self, alias: str = "champion"):
        mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
        
        model_uri = f"models:/{config.REGISTERED_MODEL_NAME}@{alias}"
        print(f"Loading model from registry: {model_uri}")
        
        try:
            # We load it via MLflow pyfunc to be framework agnostic
            self.model = mlflow.sklearn.load_model(model_uri)
        except Exception as e:
            raise RuntimeError(f"Failed to load model '{model_uri}' from MLflow Registry. Error: {e}")
            
        # We need the label map
        label_map_path = os.path.join(config.MODELS_DIR, "label_map.joblib")
        if not os.path.exists(label_map_path):
            raise FileNotFoundError("label_map.joblib not found. Please train the model first.")
            
        import joblib
        self.label_map = joblib.load(label_map_path)
        
        # Check if the loaded model uses a Pipeline internally (for TF-IDF)
        from sklearn.pipeline import Pipeline
        self.is_pipeline = isinstance(self.model, Pipeline)
        
        if not self.is_pipeline:
            self.embedding_generator = EmbeddingGenerator()
            
    def predict(self, text: str):
        cleaned = clean_text(text)
        
        if self.is_pipeline:
            # Pipeline handles TF-IDF internally
            probs = self.model.predict_proba([cleaned])[0]
        else:
            # Generate embeddings first
            embedding = self.embedding_generator.generate([cleaned])
            probs = self.model.predict_proba(embedding)[0]
            
        # Get dominant emotion
        pred_idx = np.argmax(probs)
        confidence = probs[pred_idx]
        emotion = self.label_map[pred_idx]
        
        return {
            "emotion": emotion,
            "confidence": float(confidence),
            "probabilities": {self.label_map[i]: float(probs[i]) for i in range(len(probs))}
        }

if __name__ == "__main__":
    predictor = EmotionPredictor()
    test_texts = [
        "I am so excited about this new architecture!",
        "This is really frustrating and annoying.",
        "I just feel empty inside today."
    ]
    for t in test_texts:
        res = predictor.predict(t)
        print(f"Text: {t}")
        print(f"Prediction: {res['emotion']} ({res['confidence']:.2f})\n")
