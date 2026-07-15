import pytest
from pydantic import BaseModel
from app.ai.llm.parser import OutputParser, OutputParserException

class MockSchema(BaseModel):
    name: str
    age: int

def test_output_parser_success():
    raw_json = '{"name": "Alice", "age": 30}'
    result = OutputParser.parse_pydantic(raw_json, MockSchema)
    assert result.name == "Alice"
    assert result.age == 30

def test_output_parser_markdown_stripping():
    raw_json = '```json\n{"name": "Bob", "age": 25}\n```'
    result = OutputParser.parse_pydantic(raw_json, MockSchema)
    assert result.name == "Bob"
    assert result.age == 25

def test_output_parser_invalid_json():
    raw_json = '{"name": "Alice", "age": 30' # missing closing brace
    with pytest.raises(OutputParserException) as exc:
        OutputParser.parse_pydantic(raw_json, MockSchema)
    assert "Invalid JSON" in str(exc.value)

def test_output_parser_validation_error():
    raw_json = '{"name": "Alice", "age": "thirty"}' # wrong type for age
    with pytest.raises(OutputParserException) as exc:
        OutputParser.parse_pydantic(raw_json, MockSchema)
    assert "Validation Error" in str(exc.value)
