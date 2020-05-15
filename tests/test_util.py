import logging

from pydantic import BaseModel

from openapi_schema_pydantic import Info, MediaType, OpenAPI, Operation, PathItem, RequestBody, Response
from openapi_schema_pydantic.util import PydanticSchema, construct_open_api_with_schema_class


def test_construct_open_api_with_schema_class():
    open_api = construct_base_open_api()
    open_api_1 = construct_open_api_with_schema_class(open_api, [PingRequest, PingResponse])
    open_api_2 = construct_open_api_with_schema_class(open_api, [])
    assert open_api_1.components == open_api_2.components
    assert open_api_1 == open_api_2

    open_api_json = open_api_1.json(by_alias=True, exclude_none=True, indent=2)
    logging.debug(open_api_json)


def construct_base_open_api() -> OpenAPI:
    """Construct OpenAPI using data class"""
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
                                schema=PydanticSchema(
                                    schema_class=PingRequest
                                )
                            )
                        }
                    ),
                    responses={
                        "200": Response(
                            description="pong",
                            content={
                                "application/json": MediaType(
                                    schema=PydanticSchema(
                                        schema_class=PingResponse
                                    )
                                )
                            }
                        )
                    }
                )
            )
        }
    )


class PingRequest(BaseModel):
    """Ping Request"""

    req_foo: str = ...
    """foo value of the request"""

    req_bar: str = ...
    """bar value of the request"""


class PingResponse(BaseModel):
    """Ping response"""

    resp_foo: str
    """foo value of the response"""

    resp_bar: str
    """bar value of the response"""
