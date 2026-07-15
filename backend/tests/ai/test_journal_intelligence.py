import pytest
import pytest_asyncio
from app.ai.tools.journal_intelligence import JournalIntelligenceTool, JournalIntelligenceInput
from app.schemas.journal import JournalAnalysisOutput

@pytest.fixture
def tool():
    return JournalIntelligenceTool()

def test_tool_metadata(tool):
    assert tool.name == "journal_intelligence"
    assert tool.version == "1.0.0"

def test_tool_schema(tool):
    # Test valid input schema
    input_data = {"journal_text": "I feel stressed about my exams today."}
    validated_input = tool.validate_input(input_data)
    assert isinstance(validated_input, JournalIntelligenceInput)
    assert validated_input.journal_text == input_data["journal_text"]

@pytest.mark.asyncio
async def test_tool_arun_fallback(tool):
    # This tests the fallback mock in _arun when LLM is not configured properly or fails
    result = await tool._arun(journal_text="I feel extremely sad and unmotivated today.")
    
    assert isinstance(result, dict)
    assert "summary" in result
    assert "primary_emotions" in result
    assert "stress_score" in result
    
    # Test schema validation of the output
    validated_output = tool.validate_output(result)
    assert isinstance(validated_output, JournalAnalysisOutput)
    
def test_schema_types():
    # Test that the schema properly parses dicts
    data = {
        "summary": "User is anxious",
        "primary_emotions": ["anxiety"],
        "stress_score": 8,
        "planner_metadata": {"requires_crisis_intervention": False},
        "confidence": 0.9
    }
    
    output = JournalAnalysisOutput(**data)
    assert output.summary == "User is anxious"
    assert output.stress_score == 8
    assert output.confidence == 0.9
