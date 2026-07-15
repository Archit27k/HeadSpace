from app.repositories.chat_repository import ChatRepository
from app.schemas import chat as chat_schema
from app.models.models import Session as DBSession, Conversation, Message
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

class ChatService:
    def __init__(self, db: Session):
        self.repo = ChatRepository(db)

    def get_or_create_active_session(self, user_id: UUID) -> DBSession:
        # Simplistic logic: get latest session, if not ended, use it, else create new
        sessions = self.repo.get_sessions_for_user(user_id)
        if sessions and not sessions[0].ended_at:
            return sessions[0]
        return self.repo.create_session(user_id)

    def create_conversation(self, user_id: UUID, summary: str = None) -> Conversation:
        session = self.get_or_create_active_session(user_id)
        return self.repo.create_conversation(session.id, summary)

    def get_conversation(self, user_id: UUID, conversation_id: UUID) -> Conversation:
        conv = self.repo.get_conversation(conversation_id)
        if not conv or conv.session.user_id != user_id:
            return None
        return conv

    async def add_message_stream(self, user_id: UUID, conversation_id: UUID, message: chat_schema.MessageCreate):
        conv = self.get_conversation(user_id, conversation_id)
        if not conv:
            yield "data: {\"error\": \"Conversation not found\"}\n\n"
            return
            
        # 1. Save user message to DB
        user_msg = self.repo.add_message(conversation_id, message.role, message.content)
        
        # 2. Invoke LangGraph with skip flag
        from app.ai.graph.builder import build_orchestration_graph
        graph = build_orchestration_graph()
        
        initial_state = {
            "conversation_id": str(conversation_id),
            "user_id": str(user_id),
            "messages": [{"role": "user", "content": message.content}],
            "current_intent": None,
            "emotion": {},
            "risk_assessment": None,
            "retrieved_context": [],
            "planner_decisions": {},
            "memory": {},
            "selected_tools": [],
            "tool_outputs": [],
            "validation_results": {},
            "metadata": {"skip_llm_generation": True},
            "execution_trace": []
        }
        
        final_state = await graph.ainvoke(initial_state)
        
        # 3. Stream the LLM response
        from app.ai.llm.factory import get_llm_provider
        import json
        
        provider = get_llm_provider()
        system_prompt = final_state.get("metadata", {}).get("system_prompt", "You are HeadSpace AI.")
        
        # Get message history from DB for context
        db_messages = self.repo.get_conversation(conversation_id).messages
        history_dicts = [{"role": m.role.lower(), "content": m.content} for m in db_messages[-10:]]
        
        # Also append citations if retrieved_context was found
        memory = final_state.get("memory", {})
        retrieved_items = [item for item in memory.get("ranked_context", []) if item["type"] == "retrieved_knowledge"]
        citations = []
        for i, item in enumerate(retrieved_items):
            source = item.get("metadata", {}).get("source", "Unknown Source")
            citations.append(f"[{i+1}] {source}")
            
        ai_response_content = ""
        try:
            for chunk in provider.generate_stream(history_dicts, system_message=system_prompt):
                ai_response_content += chunk
                # Yield SSE chunk
                # Note: We replace newlines with \n for JSON friendliness or just send standard SSE
                yield f"data: {json.dumps({'content': chunk})}\n\n"
                
            if citations:
                footer = "\n\nSources:\n" + "\n".join(citations)
                ai_response_content += footer
                yield f"data: {json.dumps({'content': footer})}\n\n"
                
        except Exception as e:
            import logging
            logging.error(f"Stream error: {e}")
            yield f"data: {json.dumps({'error': 'Stream error occurred.'})}\n\n"
            
        # 4. Save AI message to DB
        if ai_response_content:
            self.repo.add_message(conversation_id, "assistant", ai_response_content)
            
        # Signal end of stream
        yield "data: [DONE]\n\n"
