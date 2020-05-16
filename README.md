# openapi-schema-pydantic

OpenAPI (v3) specification schema as [Pydantic](https://github.com/samuelcolvin/pydantic) classes 

## Try me

```python
from openapi_schema_pydantic import Info, OpenAPI, Operation, PathItem, Response

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

- The [Schema Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#schemaObject)
  in OpenAPI has definitions and tweaks in JSON Schema, which is hard to comprehend and define a good data class
- Pydantic already has a good way to [create JSON schema](https://pydantic-docs.helpmanual.io/usage/schema/),
  let's not re-invent the wheel
  
The approach to deal with this:

1. Use `PydanticSchema` objects to represent the `Schema` in `OpenAPI` object
2. Invoke `construct_open_api_with_schema_class` to resolve the JSON schemas and references

```python
from pydantic import BaseModel, Field

from openapi_schema_pydantic import Info, MediaType, OpenAPI, Operation, PathItem, RequestBody, Response
from openapi_schema_pydantic.util import PydanticSchema, construct_open_api_with_schema_class

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
    req_foo: str = Field(description="foo value of the request")
    req_bar: str = Field(description="bar value of the request")

class PingResponse(BaseModel):
    """Ping response"""
    resp_foo: str = Field(description="foo value of the response")
    resp_bar: str = Field(description="bar value of the response")

open_api = construct_base_open_api()
open_api = construct_open_api_with_schema_class(open_api)

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
        "properties": {
          "req_foo": {
            "title": "Req Foo",
            "description": "foo value of the request",
            "type": "string"
          },
          "req_bar": {
            "title": "Req Bar",
            "description": "bar value of the request",
            "type": "string"
          }
        },
        "description": "Ping Request",
        "required": [
          "req_foo",
          "req_bar"
        ],
        "type": "object",
        "title": "PingRequest"
      },
      "PingResponse": {
        "properties": {
          "resp_foo": {
            "title": "Resp Foo",
            "description": "foo value of the response",
            "type": "string"
          },
          "resp_bar": {
            "title": "Resp Bar",
            "description": "bar value of the response",
            "type": "string"
          }
        },
        "description": "Ping response",
        "required": [
          "resp_foo",
          "resp_bar"
        ],
        "type": "object",
        "title": "PingResponse"
      }
    }
  }
}
```

## Note

When using `OpenAPI.json()` function, arguments `by_alias=True, exclude_none=True` has to be in place.
Otherwise the result json will not fit the OpenAPI standard.

```python
# OK
open_api.json(by_alias=True, exclude_none=True, indent=2)

# Not good
open_api.json(indent=2)
```

## License

[MIT License](https://github.com/kuimono/openapi-schema-pydantic/blob/master/LICENSE)
