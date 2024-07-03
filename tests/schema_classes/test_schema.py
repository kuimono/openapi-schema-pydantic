import logging

from pydantic import BaseModel, ConfigDict

from openapi_schema_pydantic_v2 import Schema, Reference


def test_schema():
    schema = Schema.model_validate(
        {
            "title": "reference list",
            "description": "schema for list of reference type",
            "allOf": [{"$ref": "#/definitions/TestType"}],
        }
    )
    logging.debug(f"schema.allOf={schema.allOf}")
    assert schema.allOf
    assert isinstance(schema.allOf, list)
    assert isinstance(schema.allOf[0], Reference)
    assert schema.allOf[0].ref == "#/definitions/TestType"


def test_issue_4():
    """https://github.com/kuimono/openapi-schema-pydantic/issues/4"""

    class TestModel(BaseModel):
        test_field: str

        model_config = ConfigDict(extra="forbid")

    # Generate the schema using the schema() method of the model class
    schema_definition = TestModel.model_json_schema()

    expected_schema = {
        "title": "TestModel",
        "type": "object",
        "properties": {"test_field": {"title": "Test Field", "type": "string"}},
        "required": ["test_field"],
        "additionalProperties": False,
    }

    # Check if the generated schema matches the expected schema
    assert schema_definition["properties"] == expected_schema["properties"]
    assert schema_definition["required"] == expected_schema["required"]
    assert (
        schema_definition["additionalProperties"]
        == expected_schema["additionalProperties"]
    )
    assert schema_definition["title"] == expected_schema["title"]

    # Validate the schema behavior using Pydantic's BaseModel.model_validate
    # This simulates loading and validating an object against the schema
    result = TestModel.model_validate({"test_field": "Example"})
    assert result.test_field == "Example"

    # Asserting no additional properties are allowed
    try:
        TestModel.model_validate({"test_field": "Example", "extra_field": "Not allowed"})
    except Exception as e:
        assert isinstance(e, ValueError)
