import logging

from openapi_schema_pydantic import Schema, Reference


def test_schema():
    schema = Schema.parse_obj(
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
