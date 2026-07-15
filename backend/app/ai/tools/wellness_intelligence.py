import logging
import json
from typing import Any, Dict
from pydantic import BaseModel, Field

from app.ai.tools.base import BaseTool
from app.schemas.wellness import WellnessEngineOutput
from app.ai.prompts.templates.wellness_intelligence_template import WellnessIntelligencePrompt
from app.ai.llm.factory import get_llm_provider
from app.ai.wellness.context import ContextAggregator
from app.ai.wellness.validator import SafetyValidator

logger = logging.getLogger(__name__)

class WellnessIntelligenceInput(BaseModel):
    # The tool will fetch most data from the user_context, but we can pass state if needed.
    # To conform to standard tool interfaces, we might accept an explicit string or dict.
    state_dump: str = Field("", description="JSON dump of the current graph state for context aggregation.")

class WellnessIntelligenceTool(BaseTool):
    """
    Tool that uses the Wellness Intelligence Engine to generate personalized wellness recommendations.
    """
    name: str = "wellness_intelligence"
    description: str = "Generates personalized wellness recommendations based on user context, memory, and emotions."
    version: str = "1.0.0"
    
    input_schema = WellnessIntelligenceInput
    output_schema = WellnessEngineOutput
    
    def _run(self, **kwargs) -> Any:
        raise NotImplementedError("WellnessIntelligenceTool only supports async execution.")

    async def _arun(self, **kwargs) -> Any:
        # In a robust implementation, state is passed via user_context or injected.
        # Here we assume the state is provided via kwargs for simplicity, or we mock it if missing.
        state_dump = kwargs.get("state_dump", "{}")
        try:
            state = json.loads(state_dump)
        except:
            state = {}
            
        # 1. Aggregate Context
        aggregated_context = ContextAggregator.aggregate(state)
        
        # 2. Build prompt
        prompt_template = WellnessIntelligencePrompt()
        system_prompt = prompt_template.render(aggregated_context=aggregated_context)
        
        # 3. Call LLM
        provider = get_llm_provider()
        messages = [{"role": "user", "content": "Generate personalized wellness recommendations based on my context."}]
        
        try:
            response_json = provider.generate_chat(
                messages=messages, 
                system_message=system_prompt + "\nOUTPUT ONLY VALID JSON MATCHING THE SCHEMA."
            )
            
            response_json = response_json.strip()
            if response_json.startswith("```json"):
                response_json = response_json[7:-3]
            elif response_json.startswith("```"):
                response_json = response_json[3:-3]
                
            parsed_data = json.loads(response_json)
            output = WellnessEngineOutput(**parsed_data)
            
        except Exception as e:
            logger.error(f"Failed to generate wellness recommendations: {e}")
            output = WellnessEngineOutput(
                recommendations=[],
                priority="Medium",
                reasoning="Failed to generate recommendations due to an internal error.",
                confidence=0.0
            )
            
        # 4. Safety Validation
        safe_output = SafetyValidator.validate(output, state)
        
        return safe_output.model_dump()
