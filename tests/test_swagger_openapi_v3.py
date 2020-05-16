from openapi_schema_pydantic import OpenAPI


def test_swagger_openapi_v3():
    open_api = OpenAPI.parse_file("tests/data/swagger_openapi_v3.0.1.json")
    assert open_api
