# openapi-schema-pydantic

[![PyPI](https://img.shields.io/pypi/v/openapi-schema-pydantic)](https://pypi.org/project/openapi-schema-pydantic/)
[![PyPI - License](https://img.shields.io/pypi/l/openapi-schema-pydantic)](https://github.com/kuimono/openapi-schema-pydantic/blob/master/LICENSE)

OpenAPI (v3) specification schema as [Pydantic](https://github.com/samuelcolvin/pydantic) classes.

The naming of the classes follows the schema in 
[OpenAPI specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#schema).

## Installation

`pip install openapi-schema-pydantic`

## Try me

```python
from openapi_schema_pydantic import OpenAPI, Info, PathItem, Operation, Response

# Construct OpenAPI by pydantic objects
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
    },
)
print(open_api.model_dump_json(by_alias=True, exclude_none=True, indent=2))
```

Result:

```json
{
  "openapi": "3.1.0",
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

## Take advantage of Pydantic

Pydantic is a great tool. It allows you to use object / dict / mixed data for input.
The following examples give the same OpenAPI result as above:

```python
from openapi_schema_pydantic import OpenAPI, PathItem, Response

# Construct OpenAPI from dict
open_api = OpenAPI.model_validate({
    "info": {"title": "My own API", "version": "v0.0.1"},
    "paths": {
        "/ping": {
            "get": {"responses": {"200": {"description": "pong"}}}
        }
    },
})

# Construct OpenAPI with mix of dict/object
open_api = OpenAPI.model_validate({
    "info": {"title": "My own API", "version": "v0.0.1"},
    "paths": {
        "/ping": PathItem(
            get={"responses": {"200": Response(description="pong")}}
        )
    },
})
```

## Use Pydantic classes as schema

- The [Schema Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#schemaObject)
  in OpenAPI has definitions and tweaks in JSON Schema, which are hard to comprehend and define a good data class
- Pydantic already has a good way to [create JSON schema](https://pydantic-docs.helpmanual.io/usage/schema/),
  let's not re-invent the wheel

The approach to deal with this:

1. Use `PydanticSchema` objects to represent the `Schema` in `OpenAPI` object
2. Invoke `construct_open_api_with_schema_class` to resolve the JSON schemas and references

```python
from pydantic import BaseModel, Field

from openapi_schema_pydantic import OpenAPI
from openapi_schema_pydantic.util import PydanticSchema, construct_open_api_with_schema_class

def construct_base_open_api() -> OpenAPI:
    return OpenAPI.model_validate({
        "info": {"title": "My own API", "version": "v0.0.1"},
        "paths": {
            "/ping": {
                "post": {
                    "requestBody": {"content": {"application/json": {
                        "schema": PydanticSchema(schema_class=PingRequest)
                    }}},
                    "responses": {"200": {
                        "description": "pong",
                        "content": {"application/json": {
                            "schema": PydanticSchema(schema_class=PingResponse)
                        }},
                    }},
                }
            }
        },
    })

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

# print the result of openapi.model_dump_json()
print(open_api.model_dump_json(by_alias=True, exclude_none=True, indent=2))
```

Result:

```json
{
  "openapi": "3.1.0",
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
            "type": "string",
            "title": "Req Foo",
            "description": "foo value of the request"
          },
          "req_bar": {
            "type": "string",
            "title": "Req Bar",
            "description": "bar value of the request"
          }
        },
        "type": "object",
        "required": [
          "req_foo",
          "req_bar"
        ],
        "title": "PingRequest",
        "description": "Ping Request"
      },
      "PingResponse": {
        "properties": {
          "resp_foo": {
            "type": "string",
            "title": "Resp Foo",
            "description": "foo value of the response"
          },
          "resp_bar": {
            "type": "string",
            "title": "Resp Bar",
            "description": "bar value of the response"
          }
        },
        "type": "object",
        "required": [
          "resp_foo",
          "resp_bar"
        ],
        "title": "PingResponse",
        "description": "Ping response"
      }
    }
  }
}
```

## Notes

### Use of OpenAPI.model_dump_json() / OpenAPI.model_dump()

When using `OpenAPI.model_dump_json()` / `OpenAPI.model_dump()` functions,
the arguments `by_alias=True, exclude_none=True` have to be in place,
otherwise the resulting json will not fit the OpenAPI standard.

```python
# OK
open_api.model_dump_json(by_alias=True, exclude_none=True, indent=2)

# Not good
open_api.model_dump_json(indent=2)
```

More info about field aliases:

| OpenAPI version | Field alias info |
| --------------- | ---------------- |
| 3.1.0 | [here](https://github.com/kuimono/openapi-schema-pydantic/blob/master/openapi_schema_pydantic/v3/v3_1_0/README.md#alias) |
| 3.0.3 | [here](https://github.com/kuimono/openapi-schema-pydantic/blob/master/openapi_schema_pydantic/v3/v3_0_3/README.md#alias) |

### Non-pydantic schema types

Some schema types are not implemented as pydantic classes.
Please refer to the following for more info:

| OpenAPI version | Non-pydantic schema type info |
| --------------- | ----------------------------- |
| 3.1.0 | [here](https://github.com/kuimono/openapi-schema-pydantic/blob/master/openapi_schema_pydantic/v3/v3_1_0/README.md#non-pydantic-schema-types) |
| 3.0.3 | [here](https://github.com/kuimono/openapi-schema-pydantic/blob/master/openapi_schema_pydantic/v3/v3_0_3/README.md#non-pydantic-schema-types) |

### Use OpenAPI 3.0.3 instead of 3.1.0

Some UI renderings (e.g. Swagger) still do not support OpenAPI 3.1.0.
The old 3.0.3 version is available by importing from different paths:

```python
from openapi_schema_pydantic.v3.v3_0_3 import OpenAPI, ...
from openapi_schema_pydantic.v3.v3_0_3.util import PydanticSchema, construct_open_api_with_schema_class
```

## License

[MIT License](https://github.com/kuimono/openapi-schema-pydantic/blob/master/LICENSE)
