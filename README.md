# openapi-schema-pydantic
OpenAPI (v3) specification schema as Pydantic classes 

## Try me

```python
from openapi_schema_pydantic import (
    Info,
    OpenAPI,
    Operation,
    PathItem,
    Response
)

def readme_example_1() -> OpenAPI:
    """Construct OpenAPI using data class"""
    open_api = OpenAPI(
        info=Info(
            title="My own API",
            version="v0.0.1",
        ),
        paths={
            "/ping": PathItem(
                get=Operation(
                    responses={
                        "200": Response(
                            description="pong"
                        )
                    }
                )
            )
        }
    )

    return open_api

def readme_example_2() -> OpenAPI:
    """Construct OpenAPI from raw data object"""
    open_api = OpenAPI.parse_obj({
        "info": {
            "title": "My own API",
            "version": "v0.0.1"
        },
        "paths": {
            "/ping": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "pong"
                        }
                    }
                }
            }
        }
    })

    return open_api

open_api_1 = readme_example_1()
open_api_2 = readme_example_2()
assert open_api_1 == open_api_2

# print the result openapi.json
print(open_api_1.json(by_alias=True, exclude_none=True, indent=2))
```

Result:

```json
{
  "openapi": "3.0.3",
  "info": {
    "title": "My own API",
    "version": "v0.0.1"
  },
  "servers": [
    {
      "url": "/"
    }
  ],
  "paths": {
    "/ping": {
      "get": {
        "responses": {
          "200": {
            "description": "pong"
          }
        },
        "deprecated": false
      }
    }
  }
}
```

## Use Pydantic classes as schema

```python
from pydantic import BaseModel

from openapi_schema_pydantic import (
    Info,
    MediaType,
    OpenAPI,
    Operation,
    PathItem,
    RequestBody,
    Response,
)
from openapi_schema_pydantic.util import (
    PydanticSchema,
    construct_open_api_with_schema_class,
)

def construct_base_open_api() -> OpenAPI:
    """Construct OpenAPI using data class"""
    open_api = OpenAPI(
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

    return open_api


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

open_api = construct_base_open_api()
open_api = construct_open_api_with_schema_class(open_api, [])

# print the result openapi.json
print(open_api.json(by_alias=True, exclude_none=True, indent=2))
```

Result:

```json
{
  "openapi": "3.0.3",
  "info": {
    "title": "My own API",
    "version": "v0.0.1"
  },
  "servers": [
    {
      "url": "/"
    }
  ],
  "paths": {
    "/ping": {
      "post": {
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/PingRequest"
              }
            }
          },
          "required": false
        },
        "responses": {
          "200": {
            "description": "pong",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/PingResponse"
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "components": {
    "schemas": {
      "PingRequest": {
        "required": [
          "req_foo",
          "req_bar"
        ],
        "properties": {
          "req_foo": {
            "title": "Req Foo",
            "type": "string"
          },
          "req_bar": {
            "title": "Req Bar",
            "type": "string"
          }
        },
        "title": "PingRequest",
        "description": "Ping Request",
        "type": "object"
      },
      "PingResponse": {
        "required": [
          "resp_foo",
          "resp_bar"
        ],
        "properties": {
          "resp_foo": {
            "title": "Resp Foo",
            "type": "string"
          },
          "resp_bar": {
            "title": "Resp Bar",
            "type": "string"
          }
        },
        "title": "PingResponse",
        "description": "Ping response",
        "type": "object"
      }
    }
  }
}
```

## License

[MIT License](https://github.com/kuimono/openapi-schema-pydantic/blob/master/LICENSE)
