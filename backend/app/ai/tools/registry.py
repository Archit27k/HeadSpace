from typing import Dict, Optional, List
import logging
from app.ai.tools.base import BaseTool

logger = logging.getLogger(__name__)

class ToolRegistry:
    """
    Manages the dynamic registration, discovery, and retrieval of Agent Tools.
    """
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        
    def register(self, tool: BaseTool) -> None:
        """Registers a tool in the ecosystem."""
        if tool.name in self._tools:
            logger.warning(f"Tool {tool.name} already registered. Overwriting.")
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name} (v{tool.version})")
        
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Retrieves a tool by name."""
        return self._tools.get(name)
        
    def discover(self) -> List[Dict[str, str]]:
        """Returns metadata for all available tools."""
        return [
            {
                "name": t.name,
                "description": t.description,
                "version": t.version
            }
            for t in self._tools.values()
        ]
        
    def disable(self, name: str) -> None:
        """Removes a tool from the registry."""
        if name in self._tools:
            del self._tools[name]
            logger.info(f"Disabled tool: {name}")
