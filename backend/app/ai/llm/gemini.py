from app.ai.llm.base import BaseLLMProvider
from typing import Dict, Any, List, Generator
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import os
import logging
import json

logger = logging.getLogger(__name__)

class GeminiProvider(BaseLLMProvider):
    """
    Production implementation of the Google Gemini Provider.
    Supports streaming, structured JSON, and automated retries.
    """
    def __init__(self, api_key: str = None):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            logger.warning("GEMINI_API_KEY is not set. Gemini API calls will fail.")
        else:
            genai.configure(api_key=key)
            
        # Default safety settings - adjustable per environment
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
        
        # Primary model configuration
        self.model_name = "gemini-1.5-pro-latest"
        logger.info(f"Initialized GeminiProvider using model {self.model_name}")

    def _format_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Converts internal message format to Gemini's expected Content format."""
        formatted = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            formatted.append({"role": role, "parts": [msg["content"]]})
        return formatted

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def generate(self, prompt: str, system_message: str = None) -> str:
        logger.info("Executing Gemini generate()")
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_message
        )
        response = model.generate_content(
            prompt,
            safety_settings=self.safety_settings
        )
        return response.text

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def generate_chat(self, messages: List[Dict[str, str]], system_message: str = None) -> str:
        logger.info(f"Executing Gemini generate_chat() with {len(messages)} messages")
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_message
        )
        formatted_history = self._format_messages(messages)
        chat = model.start_chat(history=formatted_history[:-1]) # Start with history
        
        # Send the latest message
        latest_msg = formatted_history[-1]["parts"][0]
        response = chat.send_message(latest_msg, safety_settings=self.safety_settings)
        return response.text

    def generate_stream(self, messages: List[Dict[str, str]], system_message: str = None) -> Generator[str, None, None]:
        logger.info(f"Executing Gemini generate_stream() with {len(messages)} messages")
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=system_message
        )
        formatted_history = self._format_messages(messages)
        chat = model.start_chat(history=formatted_history[:-1])
        
        latest_msg = formatted_history[-1]["parts"][0]
        response = chat.send_message(latest_msg, safety_settings=self.safety_settings, stream=True)
        
        for chunk in response:
            yield chunk.text

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def generate_structured(self, messages: List[Dict[str, str]], schema: Any, system_message: str = None) -> Dict[str, Any]:
        """
        Forces Gemini to output JSON matching the provided schema.
        Note: schema can be a dict for OpenAPI schema or a string definition.
        """
        logger.info("Executing Gemini generate_structured()")
        
        # Gemini 1.5 supports response_mime_type="application/json"
        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json",
            # We can optionally pass response_schema here if supported, or rely on prompt steering
        )
        
        # Append schema requirements to system message to be safe
        enhanced_system = f"{system_message or ''}\n\nOUTPUT REQUIREMENT: You MUST output ONLY valid JSON matching this schema:\n{schema}"
        
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=enhanced_system,
            generation_config=generation_config
        )
        
        formatted_history = self._format_messages(messages)
        chat = model.start_chat(history=formatted_history[:-1])
        latest_msg = formatted_history[-1]["parts"][0]
        
        response = chat.send_message(latest_msg, safety_settings=self.safety_settings)
        return json.loads(response.text)
