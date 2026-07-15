from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.models.database import get_db
from app.core.security import get_current_user
from app.services.chat_service import ChatService
from app.schemas.chat import ConversationCreate, ConversationResponse, MessageCreate, MessageResponse
from app.models.models import User

router = APIRouter()

@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(conv: ConversationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ChatService(db)
    return service.create_conversation(current_user.id, conv.summary)

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ChatService(db)
    conv = service.get_conversation(current_user.id, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

from fastapi.responses import StreamingResponse

@router.post("/conversations/{conversation_id}/messages")
async def add_message(conversation_id: UUID, message: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ChatService(db)
    
    # Check if conversation exists first
    conv = service.get_conversation(current_user.id, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    # Return streaming response
    return StreamingResponse(
        service.add_message_stream(current_user.id, conversation_id, message),
        media_type="text/event-stream"
    )
