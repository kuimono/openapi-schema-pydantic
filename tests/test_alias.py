from openapi_schema_pydantic import Header, MediaType, Parameter, PathItem, Reference, Schema, SecurityScheme


def test_header_alias():
    header_1 = Header(param_in="header")
    header_2 = Header.model_validate({"param_in": "header"})
    header_3 = Header.model_validate({"in": "header"})
    assert header_1 == header_2 == header_3


def test_media_type_alias():
    media_type_1 = MediaType(media_type_schema=Schema())
    media_type_2 = MediaType(schema=Schema())
    media_type_3 = MediaType.model_validate({"media_type_schema": Schema()})
    media_type_4 = MediaType.model_validate({"schema": Schema()})
    assert media_type_1 == media_type_2 == media_type_3 == media_type_4


def test_parameter_alias():
    parameter_1 = Parameter(name="test", param_in="path", param_schema=Schema())
    parameter_2 = Parameter(name="test", param_in="path", schema=Schema())
    parameter_3 = Parameter.model_validate({"name": "test", "param_in": "path", "param_schema": Schema()})
    parameter_4 = Parameter.model_validate({"name": "test", "in": "path", "schema": Schema()})
    assert parameter_1 == parameter_2 == parameter_3 == parameter_4


def test_path_item_alias():
    path_item_1 = PathItem(ref="#/dummy")
    path_item_2 = PathItem.model_validate({"ref": "#/dummy"})
    path_item_3 = PathItem.model_validate({"$ref": "#/dummy"})
    assert path_item_1 == path_item_2 == path_item_3


def test_reference_alias():
    reference_1 = Reference(ref="#/dummy")
    reference_2 = Reference.model_validate({"ref": "#/dummy"})
    reference_3 = Reference.model_validate({"$ref": "#/dummy"})
    assert reference_1 == reference_2 == reference_3


def test_security_scheme():
    security_scheme_1 = SecurityScheme(type="apiKey", security_scheme_in="header")
    security_scheme_2 = SecurityScheme.model_validate({"type": "apiKey", "security_scheme_in": "header"})
    security_scheme_3 = SecurityScheme.model_validate({"type": "apiKey", "in": "header"})
    assert security_scheme_1 == security_scheme_2 == security_scheme_3


def test_schema():
    schema_1 = Schema(schema_not=Schema(), schema_format="email")
    schema_2 = Schema.model_validate({"schema_not": Schema(), "schema_format": "email"})
    schema_3 = Schema.model_validate({"not": Schema(), "format": "email"})
    assert schema_1 == schema_2 == schema_3
