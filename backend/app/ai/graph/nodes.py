import time
from typing import Dict, Any
from app.ai.graph.state import GraphState
import logging

logger = logging.getLogger(__name__)

def _record_trace(node_name: str, start_time: float) -> Dict[str, Any]:
    return {
        "node": node_name,
        "execution_time_ms": round((time.time() - start_time) * 1000, 2),
        "timestamp": time.time()
    }

def conversation_entry(state: GraphState) -> Dict[str, Any]:
    """Initializes the conversation state and metadata."""
    start_time = time.time()
    # In a real app, this might fetch initial user metadata or session info
    return {
        "metadata": {"status": "initialized"},
        "execution_trace": [_record_trace("conversation_entry", start_time)]
    }

def intent_detection(state: GraphState) -> Dict[str, Any]:
    """Analyzes the latest message to determine user intent."""
    start_time = time.time()
    latest_message = state["messages"][-1]["content"] if state.get("messages") else ""
    
    # Placeholder logic for intent detection
    intent = "general_chat"
    if "journal" in latest_message.lower():
        intent = "journal_entry"
    elif "help" in latest_message.lower() or "crisis" in latest_message.lower():
        intent = "crisis_support"
        
    return {
        "current_intent": intent,
        "execution_trace": [_record_trace("intent_detection", start_time)]
    }

def planner(state: GraphState) -> Dict[str, Any]:
    """Decides which tools, memory, or RAG systems to query based on intent."""
    start_time = time.time()
    intent = state.get("current_intent", "general_chat")
    
    decisions = {
        "use_rag": intent in ["journal_query", "general_chat"],
        "use_tools": intent == "journal_entry",
        "requires_emotion_detection": True
    }
    
    return {
        "planner_decisions": decisions,
        "execution_trace": [_record_trace("planner", start_time)]
    }

from app.ai.memory.manager import MemoryCoordinator
from uuid import UUID
import uuid

def memory_manager(state: GraphState) -> Dict[str, Any]:
    """Retrieves or updates short-term and long-term memory via MemoryCoordinator."""
    start_time = time.time()
    
    from app.models.database import SessionLocal
    db = SessionLocal()
    try:
        coordinator = MemoryCoordinator(db=db)
        
        # Extract identifiers from state
        user_id_str = state.get("user_id")
        session_id_str = state.get("conversation_id") # Treat conversation as session for memory scope
        
        try:
            user_id = UUID(user_id_str) if user_id_str else uuid.uuid4()
            session_id = UUID(session_id_str) if session_id_str else uuid.uuid4()
        except (ValueError, TypeError):
            user_id = uuid.uuid4()
            session_id = uuid.uuid4()
            
        intent = state.get("current_intent", "general_chat")
        
        # Store incoming context
        coordinator.store_context(user_id, session_id, intent, state)
        
        # Retrieve relevant past context
        context = coordinator.retrieve_context(user_id, session_id, query=intent, state=state)
        
    finally:
        db.close()
        
    return {
        "memory": context,
        "execution_trace": [_record_trace("memory_manager", start_time)]
    }

def emotion_service(state: GraphState) -> Dict[str, Any]:
    """Interfaces with the Emotion Predictor to analyze user mood."""
    start_time = time.time()
    # Placeholder: Will eventually call app.services.inference.InferenceService
    emotion = {"primary": "neutral", "confidence": 0.8}
    
    return {
        "emotion": emotion,
        "execution_trace": [_record_trace("emotion_service", start_time)]
    }

def retriever(state: GraphState) -> Dict[str, Any]:
    """Queries vector stores if RAG is required by the planner."""
    start_time = time.time()
    decisions = state.get("planner_decisions", {})
    context = []
    
    if decisions.get("use_rag"):
        # Placeholder for vector store retrieval
        context = [{"source": "journal_id_123", "content": "Past journal context placeholder."}]
        
    return {
        "retrieved_context": context,
        "execution_trace": [_record_trace("retriever", start_time)]
    }

from app.ai.prompts.builder import PromptBuilder
from app.ai.prompts.registry import prompt_registry
from app.ai.prompts.templates.system import SystemChatPrompt
from app.ai.llm.factory import get_llm_provider
from app.ai.llm.parser import OutputParser, OutputParserException
from pydantic import BaseModel

# Register the core prompt template (In a real app, this might happen at startup)
prompt_registry.register(SystemChatPrompt())

def prompt_builder(state: GraphState) -> Dict[str, Any]:
    """Constructs the final system prompt with context, emotion, and memory."""
    start_time = time.time()
    
    # We use our new PromptBuilder
    # For now, we mock user_metadata
    user_metadata = {"first_name": "User"}
    
    try:
        system_prompt = PromptBuilder.build_system_prompt("system_chat", state, user_metadata)
    except Exception as e:
        logger.error(f"Failed to build prompt: {e}")
        system_prompt = "You are HeadSpace AI. Be helpful."
        
    metadata_update = state.get("metadata", {})
    
    # Apply Safety Override if present
    safety_override = metadata_update.get("safety_prompt_override")
    if safety_override:
        system_prompt = f"{system_prompt}\n\n[SAFETY OVERRIDE]\n{safety_override}"
        
    metadata_update["prompt_built"] = True
    metadata_update["system_prompt"] = system_prompt
    
    return {
        "metadata": metadata_update,
        "execution_trace": [_record_trace("prompt_builder", start_time)]
    }

def llm_provider(state: GraphState) -> Dict[str, Any]:
    """Calls the configured LLM provider to generate a response."""
    start_time = time.time()
    
    provider = get_llm_provider()
    messages = state.get("messages", [])
    system_prompt = state.get("metadata", {}).get("system_prompt")
    
    # Simple validation
    if not messages:
        messages = [{"role": "user", "content": "Hello"}]
    if state.get("metadata", {}).get("skip_llm_generation"):
        return {
            "messages": [{"role": "assistant", "content": "STREAMING_PLACEHOLDER"}],
            "execution_trace": [_record_trace("llm_provider_skipped", start_time)]
        }
        
    try:
        # In a real environment with a valid API key, this would hit Gemini.
        # Since we might not have a real key during these tests, we wrap it.
        # provider.generate_chat uses the Tenacity retry decorator internally.
        response_text = provider.generate_chat(messages, system_message=system_prompt)
    except Exception as e:
        logger.error(f"LLM Generation failed: {e}")
        response_text = "I'm having trouble connecting to my brain right now. Please try again later."
        
    response_msg = {"role": "assistant", "content": response_text}
    
    return {
        "messages": [response_msg],
        "tool_outputs": state.get("tool_outputs", []),
        "execution_trace": [_record_trace("llm_provider", start_time)]
    }

class ModerationSchema(BaseModel):
    is_safe: bool
    flagged: bool
    reason: str = ""

def response_validator(state: GraphState) -> Dict[str, Any]:
    """Ensures safety, structural validity, and policy alignment of the response."""
    start_time = time.time()
    
    
    if state.get("metadata", {}).get("skip_llm_generation"):
        return {"execution_trace": [_record_trace("response_validator_skipped", start_time)]}

    # We can use the OutputParser to optionally validate JSON
    # For a general chat response, we just do a simple check.
    # If the response was supposed to be structured, we would parse it here.
    
    latest_response = state.get("messages", [])[-1]["content"] if state.get("messages") else ""
    
    validation = {"is_safe": True, "flagged": False}
    if "kill" in latest_response.lower() or "harm" in latest_response.lower():
        validation["is_safe"] = False
        validation["flagged"] = True
        
    return {
        "validation_results": validation,
        "execution_trace": [_record_trace("response_validator", start_time)]
    }

from app.ai.emotion.classifier import MLflowEmotionService

# Can be dependency injected in real app
emotion_classifier = MLflowEmotionService()

from app.ai.tools.router import ToolRouter
from app.ai.tools.engine import ToolExecutionEngine
from app.ai.tools.registry import ToolRegistry
from app.ai.tools.journal_intelligence import JournalIntelligenceTool
from app.ai.tools.safety_tools import EmergencyResourceTool, GroundingTool
from app.ai.tools.wellness_intelligence import WellnessIntelligenceTool

# Mock Tool Registry setup
registry = ToolRegistry()
registry.register(JournalIntelligenceTool())
registry.register(EmergencyResourceTool())
registry.register(GroundingTool())
registry.register(WellnessIntelligenceTool())
engine = ToolExecutionEngine(registry)

from app.ai.safety.intervention import InterventionEngine
from app.schemas.safety import RiskAssessment, RiskLevel
from app.ai.safety.policies import get_policy

def planner(state: GraphState) -> Dict[str, Any]:
    """Analyzes the request and risk assessment to determine required actions and context."""
    start_time = time.time()
    
    metadata_update = state.get("metadata", {})
    
    # 1. Evaluate Risk Assessment
    risk_dict = state.get("risk_assessment")
    selected_tools = []
    
    if risk_dict:
        risk_assessment = RiskAssessment(**risk_dict)
        policy = get_policy(risk_assessment.risk_level)
        
        if policy.override_planner or policy.mandatory_intervention:
            state["current_intent"] = "crisis_support"
            selected_tools = InterventionEngine.get_intervention_tools(risk_assessment)
            
            # Add safety prompt overrides
            if policy.system_prompt_override:
                metadata_update["safety_prompt_override"] = policy.system_prompt_override
                
    # 2. Normal Planner Logic (if not overridden)
    if not selected_tools and not (risk_dict and get_policy(RiskAssessment(**risk_dict).risk_level).override_planner):
        current_emotion_res = state.get("metadata", {}).get("current_emotion", None)
        if current_emotion_res and getattr(current_emotion_res, "risk_score", 0.0) > 0.7:
            state["current_intent"] = "crisis_support"
        else:
            if not state.get("current_intent"):
                state["current_intent"] = "general_chat"
                
        # Add latest message to metadata for tools that need the raw text (like Journal Intelligence)
        messages = state.get("messages", [])
        if messages:
            metadata_update["latest_message"] = messages[-1].get("content", "")

        # Tool Router integration
        selected_tools = ToolRouter.parse_requested_tools(state.get("current_intent"), metadata_update)
            
    metadata_update["planner_executed"] = True
    
    return {
        "current_intent": state.get("current_intent"),
        "selected_tools": selected_tools,
        "metadata": metadata_update,
        "execution_trace": [_record_trace("planner", start_time)]
    }

async def tool_execution(state: GraphState) -> Dict[str, Any]:
    """Safely executes the tools requested by the planner."""
    start_time = time.time()
    selected_tools = state.get("selected_tools", [])
    
    tool_outputs = []
    user_context = {"user_id": state.get("user_id")}
    
    for tool_req in selected_tools:
        result = await engine.execute_tool(
            tool_name=tool_req["name"],
            arguments=tool_req.get("arguments", {}),
            user_context=user_context
        )
        tool_outputs.append(result)
        
    return {
        "tool_outputs": tool_outputs,
        "execution_trace": [_record_trace("tool_execution", start_time)]
    }

def emotion_service(state: GraphState) -> Dict[str, Any]:
    """Detects emotional state from the conversation to adjust AI persona."""
    start_time = time.time()
    
    messages = state.get("messages", [])
    if not messages:
        return {"execution_trace": [_record_trace("emotion_service", start_time)]}
        
    latest_msg = messages[-1].get("content", "")
    
    try:
        emotion_result = emotion_classifier.predict(latest_msg)
        logger.info(f"Emotion detected: {emotion_result.primary_emotion} (Risk: {emotion_result.risk_score})")
    except Exception as e:
        logger.error(f"Emotion classification failed: {e}")
        emotion_result = None
        
    metadata_update = state.get("metadata", {})
    if emotion_result:
        metadata_update["current_emotion"] = emotion_result
        
        # In a full implementation, we would persist this to EmotionTimelineItem DB here
        # db.add(EmotionTimelineItem(...))
    
    return {
        "metadata": metadata_update,
        "execution_trace": [_record_trace("emotion_service", start_time)]
    }

def persistence(state: GraphState) -> Dict[str, Any]:
    """Saves the final state, messages, and memory updates to the database."""
    start_time = time.time()
    metadata_update = state.get("metadata", {})
    
    # Actually save memory updates to DB
    tool_outputs = state.get("tool_outputs", [])
    user_id_str = state.get("user_id")
    
    from app.models.database import SessionLocal
    from app.models.models import LongTermMemoryItem, EmotionTimelineItem
    import uuid
    import json
    
    try:
        user_id = uuid.UUID(user_id_str)
        db = SessionLocal()
        
        # Extract Memory updates from tools (like journal intelligence)
        for output in tool_outputs:
            if isinstance(output, dict) and "memory_updates" in output:
                for mem in output["memory_updates"]:
                    # Assume mem is a dict with content and category
                    item = LongTermMemoryItem(
                        user_id=user_id,
                        content=mem.get("content", ""),
                        category=mem.get("category", "General"),
                        importance_score=mem.get("importance_score", 0.5)
                    )
                    db.add(item)
                    
        # Persist Emotion if detected
        current_emotion = metadata_update.get("current_emotion")
        if current_emotion:
            emo_item = EmotionTimelineItem(
                user_id=user_id,
                primary_emotion=getattr(current_emotion, "primary_emotion", "unknown"),
                secondary_emotions=getattr(current_emotion, "secondary_emotions", []),
                confidence=getattr(current_emotion, "confidence", 1.0),
                risk_score=getattr(current_emotion, "risk_score", 0.0),
                intensity=getattr(current_emotion, "intensity", 5),
                context_tags=getattr(current_emotion, "context_tags", [])
            )
            db.add(emo_item)
            
        db.commit()
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Persistence failed: {e}")
        if 'db' in locals():
            db.rollback()
    finally:
        if 'db' in locals():
            db.close()
            
    metadata_update["persisted"] = True
    
    return {
        "metadata": metadata_update,
        "execution_trace": [_record_trace("persistence", start_time)]
    }

def response_node(state: GraphState) -> Dict[str, Any]:
    """Final node that formats the output for the client."""
    start_time = time.time()
    # We do not need to modify state here heavily, just finalize execution
    return {
        "execution_trace": [_record_trace("response_node", start_time)]
    }
