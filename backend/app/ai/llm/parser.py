import json
from typing import Any, Dict, Type
from pydantic import BaseModel, ValidationError
import logging

logger = logging.getLogger(__name__)

class OutputParserException(Exception):
    """Custom exception for LLM output parsing failures."""
    pass

class OutputParser:
    """
    Parses and validates LLM outputs against expected JSON or Pydantic schemas.
    """
    
    @staticmethod
    def parse_pydantic(raw_output: str, model: Type[BaseModel]) -> BaseModel:
        """
        Parses a raw LLM output string into a Pydantic model.
        Handles stripping markdown formatting (e.g. ```json ... ```).
        """
        cleaned_output = raw_output.strip()
        
        # Strip markdown JSON formatting if present
        if cleaned_output.startswith("```json"):
            cleaned_output = cleaned_output[7:]
        if cleaned_output.startswith("```"):
            cleaned_output = cleaned_output[3:]
        if cleaned_output.endswith("```"):
            cleaned_output = cleaned_output[:-3]
            
        cleaned_output = cleaned_output.strip()
        
        try:
            parsed_dict = json.loads(cleaned_output)
            return model(**parsed_dict)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from LLM output: {e}")
            raise OutputParserException(f"Invalid JSON: {e}")
        except ValidationError as e:
            logger.error(f"LLM output failed Pydantic validation: {e}")
            raise OutputParserException(f"Validation Error: {e}")
