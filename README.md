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
print(open_api_1.json(exclude_none=True, indent=2))
```

## Use Pydantic classes as schema

TODO: add description