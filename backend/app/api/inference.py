from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.inference import InferenceService
from app.core.security import get_current_user
from app.models.models import User

router = APIRouter()
inference_service = InferenceService()

class EmotionRequest(BaseModel):
    text: str

@router.post("/predict_emotion")
async def predict_emotion(request: EmotionRequest, current_user: User = Depends(get_current_user)):
    if not inference_service.ready:
        raise HTTPException(status_code=503, detail="Model is currently loading or unavailable")
        
    prediction = inference_service.predictor.predict(request.text)
    return {"prediction": prediction, "user_id": str(current_user.id)}
