import logging

from pydantic import BaseModel, ConfigDict
from pydantic.json_schema import models_json_schema

from openapi_schema_pydantic import Schema, Reference


def test_schema():
    schema = Schema.model_validate(
        {
            "title": "reference list",
            "description": "schema for list of reference type",
            "allOf": [{"$ref": "#/components/schemas/TestType"}],
        }
    )
    logging.debug(f"schema.allOf={schema.allOf}")
    assert schema.allOf
    assert isinstance(schema.allOf, list)
    assert isinstance(schema.allOf[0], Reference)
    assert schema.allOf[0].ref == "#/components/schemas/TestType"


def test_issue_4():
    """https://github.com/kuimono/openapi-schema-pydantic/issues/4"""

    class TestModel(BaseModel):
        test_field: str

        model_config = ConfigDict(extra="forbid")

    _key_map, schema_definition = models_json_schema([(TestModel, "validation")])
    assert schema_definition == {
        "$defs": {
            "TestModel": {
                "title": "TestModel",
                "type": "object",
                "properties": {"test_field": {"title": "Test Field", "type": "string"}},
                "required": ["test_field"],
                "additionalProperties": False,
            }
        }
    }

    # allow "additionalProperties" to have boolean value
    result = Schema.model_validate(schema_definition["$defs"]["TestModel"])
    assert result.additionalProperties is False
