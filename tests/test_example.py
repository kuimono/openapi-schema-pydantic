import logging

from openapi_schema_pydantic import Info, OpenAPI, Operation, PathItem, Response


def test_readme_example():
    open_api_1 = readme_example_1()
    assert open_api_1
    open_api_json_1 = open_api_1.json(by_alias=True, exclude_none=True, indent=2)
    logging.debug(open_api_json_1)
    assert open_api_json_1

    open_api_2 = readme_example_2()
    assert open_api_1 == open_api_2

    open_api_3 = readme_example_3()
    assert open_api_1 == open_api_3


def readme_example_1() -> OpenAPI:
    """Construct OpenAPI using data class"""
    return OpenAPI(
        info=Info(title="My own API", version="v0.0.1",),
        paths={"/ping": PathItem(get=Operation(responses={"200": Response(description="pong")}))},
    )


def readme_example_2() -> OpenAPI:
    """Construct OpenAPI from raw data object"""
    return OpenAPI.parse_obj(
        {
            "info": {"title": "My own API", "version": "v0.0.1"},
            "paths": {"/ping": {"get": {"responses": {"200": {"description": "pong"}}}}},
        }
    )


def readme_example_3() -> OpenAPI:
    """Construct OpenAPI from mixed object"""
    return OpenAPI.parse_obj(
        {
            "info": {"title": "My own API", "version": "v0.0.1"},
            "paths": {"/ping": PathItem(get={"responses": {"200": Response(description="pong")}})},
        }
    )
