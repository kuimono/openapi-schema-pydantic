from openapi_schema_pydantic.v3.v3_1_0.schema import Schema


def test_empty_schema():
    schema = Schema.model_validate({})
    assert schema == Schema()
