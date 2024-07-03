from typing_extensions import Literal
from typing import Union

from pydantic import BaseModel, Field

from openapi_schema_pydantic_v2 import (
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
from openapi_schema_pydantic_v2.util import (
    PydanticSchema,
    construct_open_api_with_schema_class,
)


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
                            "application/json": MediaType(
                                media_type_schema=PydanticSchema(
                                    schema_class=RequestModel
                                )
                            )
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


def test_pydantic_discriminator_schema_generation():
    """https://github.com/kuimono/openapi-schema-pydantic/issues/8"""

    json_schema = RequestModel.model_json_schema()
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
        },
        "properties": {
            "data": {
                "discriminator": {
                    "mapping": {"a": "#/$defs/DataAModel", "b": "#/$defs/DataBModel"},
                    "propertyName": "kind",
                },
                "oneOf": [
                    {"$ref": "#/$defs/DataAModel"},
                    {"$ref": "#/$defs/DataBModel"},
                ],
                "title": "Data",
            }
        },
        "required": ["data"],
        "title": "RequestModel",
        "type": "object",
    }


def test_pydantic_discriminator_openapi_generation():
    """https://github.com/kuimono/openapi-schema-pydantic/issues/8"""

    open_api = construct_open_api_with_schema_class(construct_base_open_api())
    json_schema = open_api.components.schemas["RequestModel"]

    assert json_schema.properties == {
        "data": Schema(
            allOf=None,
            anyOf=None,
            oneOf=[
                Reference(ref="#/$defs/DataAModel", summary=None, description=None),
                Reference(ref="#/$defs/DataBModel", summary=None, description=None),
            ],
            schema_not=None,
            schema_if=None,
            then=None,
            schema_else=None,
            dependentSchemas=None,
            prefixItems=None,
            items=None,
            contains=None,
            properties=None,
            patternProperties=None,
            additionalProperties=None,
            propertyNames=None,
            unevaluatedItems=None,
            unevaluatedProperties=None,
            type=None,
            enum=None,
            const=None,
            multipleOf=None,
            maximum=None,
            exclusiveMaximum=None,
            minimum=None,
            exclusiveMinimum=None,
            maxLength=None,
            minLength=None,
            pattern=None,
            maxItems=None,
            minItems=None,
            uniqueItems=None,
            maxContains=None,
            minContains=None,
            maxProperties=None,
            minProperties=None,
            required=None,
            dependentRequired=None,
            schema_format=None,
            contentEncoding=None,
            contentMediaType=None,
            contentSchema=None,
            title="Data",
            description=None,
            default=None,
            deprecated=None,
            readOnly=None,
            writeOnly=None,
            examples=None,
            discriminator=Discriminator(
                propertyName="kind",
                mapping={"a": "#/$defs/DataAModel", "b": "#/$defs/DataBModel"},
            ),
            xml=None,
            externalDocs=None,
            example=None,
        )
    }
