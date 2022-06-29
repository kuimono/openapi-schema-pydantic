import pytest
from pydantic import ValidationError

from openapi_schema_pydantic.v3.v3_1_0 import Schema


@pytest.mark.parametrize(
    "datatype",
    (
        "string",
        "number",
        "integer",
        "boolean",
        "array",
        "object",
        "null",
    ),
)
def test_good_types_parse_and_equate(datatype: str):
    assert Schema(type=datatype).type == datatype


def test_bad_types_raise_validation_errors():
    with pytest.raises(ValidationError):
        Schema(type="invalid")

    with pytest.raises(ValidationError):
        Schema(anyOf=[{"type": "invalid"}])

    with pytest.raises(ValidationError):
        Schema(
            properties={
                "a": Schema(type="invalid"),
            },
        )
