from typing import Dict, Any, List

class ToolRouter:
    """
    Parses planner intent and extracts requested tools.
    """
    
    @staticmethod
    def parse_requested_tools(current_intent: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        In a production agent, the LLM Planner returns a JSON structure containing
        tools to run. We simulate parsing that logic here.
        """
        requested = []
        
        # Example routing logic: if intent requires retrieving a profile
        if current_intent == "fetch_profile":
            requested.append({
                "name": "MockProfileTool",
                "arguments": {"user_id": metadata.get("user_id", "default")}
            })
            
        if current_intent == "journal_entry":
            requested.append({
                "name": "journal_intelligence",
                "arguments": {"journal_text": metadata.get("latest_message", "")}
            })
            
        if current_intent == "seek_guidance":
            import json
            # To pass the state we'll need it in the metadata. For now, we mock the state dump
            # by passing a subset of metadata. In reality, the engine has access to user_context.
            state_subset = {"metadata": metadata}
            requested.append({
                "name": "wellness_intelligence",
                "arguments": {"state_dump": json.dumps(state_subset)}
            })
            
        return requested
