from app.ai.llm.base import BaseLLMProvider
from app.ai.llm.gemini import GeminiProvider
from app.ai.llm.openai import OpenAIProvider
import os
import logging

logger = logging.getLogger(__name__)

def get_llm_provider() -> BaseLLMProvider:
    """
    Factory function to get the configured LLM provider.
    Defaults to Gemini.
    """
    provider_name = os.getenv("LLM_PROVIDER", "gemini").lower()
    logger.info(f"Instantiating LLM provider: {provider_name}")
    
    if provider_name == "gemini":
        return GeminiProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    else:
        logger.warning(f"Unknown provider '{provider_name}', defaulting to Gemini.")
        return GeminiProvider()
