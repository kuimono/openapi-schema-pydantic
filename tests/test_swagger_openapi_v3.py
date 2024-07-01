from typing import Dict, Optional

from pydantic import ConfigDict, Field

from openapi_schema_pydantic import OpenAPI, Operation, PathItem


def test_swagger_openapi_v3():
    open_api = ExtendedOpenAPI.parse_file("tests/data/swagger_openapi_v3.0.1.json")
    assert open_api


class ExtendedOperation(Operation):
    """Override classes to use "x-codegen-request-body-name" in Operation"""

    xCodegenRequestBodyName: Optional[str] = Field(default=None, alias="x-codegen-request-body-name")
    model_config = ConfigDict(populate_by_name=True)


class ExtendedPathItem(PathItem):
    get: Optional[ExtendedOperation] = None
    put: Optional[ExtendedOperation] = None
    post: Optional[ExtendedOperation] = None
    delete: Optional[ExtendedOperation] = None
    options: Optional[ExtendedOperation] = None
    head: Optional[ExtendedOperation] = None
    patch: Optional[ExtendedOperation] = None
    trace: Optional[ExtendedOperation] = None


class ExtendedOpenAPI(OpenAPI):
    paths: Dict[str, ExtendedPathItem] = ...
