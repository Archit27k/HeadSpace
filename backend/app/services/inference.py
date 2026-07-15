import os
import sys

# Hack to allow importing from ml_pipeline temporarily for the placeholder
# In production, the ML pipeline might be a separate service or installed as a package.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml_pipeline"))) # local
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../ml_pipeline"))) # docker

from ml_pipeline.predict import EmotionPredictor

class InferenceService:
    def __init__(self, alias: str = "champion"):
        try:
            self.predictor = EmotionPredictor(alias=alias)
            self.ready = True
        except Exception as e:
            print(f"Warning: Inference service could not load model. {e}")
            self.ready = False
            
    def predict_emotion(self, text: str):
        if not self.ready:
            return {"error": "Model not loaded. Please train the ML pipeline first."}
            
        return self.predictor.predict(text)

inference_service = InferenceService()
