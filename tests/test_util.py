import logging

from pydantic import BaseModel, Field

from openapi_schema_pydantic import Info, MediaType, OpenAPI, Operation, PathItem, Reference, RequestBody, Response
from openapi_schema_pydantic.util import PydanticSchema, construct_open_api_with_schema_class


def test_construct_open_api_with_schema_class_1():
    open_api = construct_base_open_api_1()
    result_open_api_1 = construct_open_api_with_schema_class(open_api)
    result_open_api_2 = construct_open_api_with_schema_class(open_api, [PingRequest, PingResponse])
    assert result_open_api_1.components == result_open_api_2.components
    assert result_open_api_1 == result_open_api_2

    open_api_json = result_open_api_1.json(by_alias=True, exclude_none=True, indent=2)
    logging.debug(open_api_json)


def test_construct_open_api_with_schema_class_2():
    open_api_1 = construct_base_open_api_1()
    open_api_2 = construct_base_open_api_2()
    result_open_api_1 = construct_open_api_with_schema_class(open_api_1)
    result_open_api_2 = construct_open_api_with_schema_class(open_api_2, [PingRequest, PingResponse])
    assert result_open_api_1 == result_open_api_2


def construct_base_open_api_1() -> OpenAPI:
    """Construct OpenAPI using data class"""
    return OpenAPI(
        info=Info(title="My own API", version="v0.0.1",),
        paths={
            "/ping": PathItem(
                post=Operation(
                    requestBody=RequestBody(
                        content={"application/json": MediaType(schema=PydanticSchema(schema_class=PingRequest))}
                    ),
                    responses={
                        "200": Response(
                            description="pong",
                            content={"application/json": MediaType(schema=PydanticSchema(schema_class=PingResponse))},
                        )
                    },
                )
            )
        },
    )


def construct_base_open_api_2() -> OpenAPI:
    """Construct OpenAPI using data class"""
    return OpenAPI(
        info=Info(title="My own API", version="v0.0.1",),
        paths={
            "/ping": PathItem(
                post=Operation(
                    requestBody=RequestBody(
                        content={
                            "application/json": MediaType(schema=Reference(ref="#/components/schemas/PingRequest"))
                        }
                    ),
                    responses={
                        "200": Response(
                            description="pong",
                            content={
                                "application/json": MediaType(schema=Reference(ref="#/components/schemas/PingResponse"))
                            },
                        )
                    },
                )
            )
        },
    )


class PingRequest(BaseModel):
    """Ping Request"""

    req_foo: str = Field(description="foo value of the request")
    req_bar: str = Field(description="bar value of the request")


class PingResponse(BaseModel):
    """Ping response"""

    resp_foo: str = Field(description="foo value of the response")
    resp_bar: str = Field(description="bar value of the response")
