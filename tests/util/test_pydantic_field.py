from typing_extensions import Literal
from typing import Union

from pydantic import BaseModel, Field
from pydantic.json_schema import models_json_schema

from openapi_schema_pydantic import (
    OpenAPI,
    Info,
    PathItem,
    Operation,
    RequestBody,
    MediaType,
    Response,
    Schema,
    Reference,
    Discriminator,
)
from openapi_schema_pydantic.util import PydanticSchema, construct_open_api_with_schema_class


def test_pydantic_discriminator_schema_generation():
    """https://github.com/kuimono/openapi-schema-pydantic/issues/8"""

    _key_map, json_schema = models_json_schema([(RequestModel, "validation")])
    assert json_schema == {
        "$defs": {
            "DataAModel": {
                "properties": {"kind": {"const": "a", "title": "Kind"}},
                "required": ["kind"],
                "title": "DataAModel",
                "type": "object",
            },
            "DataBModel": {
                "properties": {"kind": {"const": "b", "title": "Kind"}},
                "required": ["kind"],
                "title": "DataBModel",
                "type": "object",
            },
            "RequestModel": {
                "properties": {
                    "data": {
                        "discriminator": {
                            "mapping": {"a": "#/$defs/DataAModel", "b": "#/$defs/DataBModel"},
                            "propertyName": "kind",
                        },
                        "oneOf": [{"$ref": "#/$defs/DataAModel"}, {"$ref": "#/$defs/DataBModel"}],
                        "title": "Data",
                    }
                },
                "required": ["data"],
                "title": "RequestModel",
                "type": "object",
            },
        }
    }


def test_pydantic_discriminator_openapi_generation():
    """https://github.com/kuimono/openapi-schema-pydantic/issues/8"""

    open_api = construct_open_api_with_schema_class(construct_base_open_api())
    assert open_api.components is not None
    assert open_api.components.schemas is not None
    json_schema = open_api.components.schemas["RequestModel"]
    assert json_schema.properties == {
        "data": Schema(
            oneOf=[
                Reference(ref="#/components/schemas/DataAModel", summary=None, description=None),
                Reference(ref="#/components/schemas/DataBModel", summary=None, description=None),
            ],
            title="Data",
            discriminator=Discriminator(
                propertyName="kind",
                mapping={"a": "#/components/schemas/DataAModel", "b": "#/components/schemas/DataBModel"},
            ),
        )
    }


def construct_base_open_api() -> OpenAPI:
    return OpenAPI(
        info=Info(
            title="My own API",
            version="v0.0.1",
        ),
        paths={
            "/ping": PathItem(
                post=Operation(
                    requestBody=RequestBody(
                        content={
                            "application/json": MediaType(media_type_schema=PydanticSchema(schema_class=RequestModel))
                        }
                    ),
                    responses={"200": Response(description="pong")},
                )
            )
        },
    )


class DataAModel(BaseModel):
    kind: Literal["a"]


class DataBModel(BaseModel):
    kind: Literal["b"]


class RequestModel(BaseModel):
    data: Union[DataAModel, DataBModel] = Field(discriminator="kind")
