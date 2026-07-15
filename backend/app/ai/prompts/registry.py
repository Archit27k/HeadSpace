from typing import Dict, Type
from app.ai.prompts.base import BasePromptTemplate
import logging

logger = logging.getLogger(__name__)

class PromptRegistry:
    """
    Central registry for all prompt templates.
    Allows dynamic fetching of prompts by name and ensures they comply 
    with the BasePromptTemplate interface.
    """
    def __init__(self):
        self._prompts: Dict[str, BasePromptTemplate] = {}
        
    def register(self, template: BasePromptTemplate) -> None:
        """Registers a prompt template instance."""
        if template.name in self._prompts:
            logger.warning(f"Overwriting existing prompt template: {template.name}")
            
        self._prompts[template.name] = template
        logger.info(f"Registered prompt template: {template.name} (v{template.version})")
        
    def get(self, name: str) -> BasePromptTemplate:
        """Retrieves a prompt template by name."""
        if name not in self._prompts:
            raise KeyError(f"Prompt template '{name}' not found in registry.")
        return self._prompts[name]
        
    def get_all(self) -> Dict[str, str]:
        """Returns a dict of all registered prompt names and their versions."""
        return {name: tpl.version for name, tpl in self._prompts.items()}

# Global Singleton Registry
prompt_registry = PromptRegistry()
