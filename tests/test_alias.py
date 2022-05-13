from openapi_schema_pydantic import Header, MediaType, Parameter, ParameterLocation, PathItem, Reference, Schema, SecurityScheme


def test_header_alias():
    header_1 = Header(param_in="header")
    header_2 = Header.parse_obj({"param_in": "header"})
    header_3 = Header.parse_obj({"in": "header"})
    header_4 = Header.parse_obj({"in": ParameterLocation.HEADER})
    assert header_1 == header_2 == header_3 == header_4


def test_media_type_alias():
    media_type_1 = MediaType(media_type_schema=Schema())
    media_type_2 = MediaType(schema=Schema())
    media_type_3 = MediaType.parse_obj({"media_type_schema": Schema()})
    media_type_4 = MediaType.parse_obj({"schema": Schema()})
    assert media_type_1 == media_type_2 == media_type_3 == media_type_4


def test_parameter_alias():
    parameter_1 = Parameter(name="test", param_in="path", param_schema=Schema())
    parameter_2 = Parameter(name="test", param_in="path", schema=Schema())
    parameter_3 = Parameter.parse_obj({"name": "test", "param_in": "path", "param_schema": Schema()})
    parameter_4 = Parameter.parse_obj({"name": "test", "in": "path", "schema": Schema()})
    assert parameter_1 == parameter_2 == parameter_3 == parameter_4


def test_path_item_alias():
    path_item_1 = PathItem(ref="#/dummy")
    path_item_2 = PathItem.parse_obj({"ref": "#/dummy"})
    path_item_3 = PathItem.parse_obj({"$ref": "#/dummy"})
    assert path_item_1 == path_item_2 == path_item_3


def test_reference_alias():
    reference_1 = Reference(ref="#/dummy")
    reference_2 = Reference.parse_obj({"ref": "#/dummy"})
    reference_3 = Reference.parse_obj({"$ref": "#/dummy"})
    assert reference_1 == reference_2 == reference_3


def test_security_scheme():
    security_scheme_1 = SecurityScheme(type="apiKey", security_scheme_in="header")
    security_scheme_2 = SecurityScheme.parse_obj({"type": "apiKey", "security_scheme_in": "header"})
    security_scheme_3 = SecurityScheme.parse_obj({"type": "apiKey", "in": "header"})
    assert security_scheme_1 == security_scheme_2 == security_scheme_3


def test_schema():
    schema_1 = Schema(schema_not=Schema(), schema_format="email")
    schema_2 = Schema.parse_obj({"schema_not": Schema(), "schema_format": "email"})
    schema_3 = Schema.parse_obj({"not": Schema(), "format": "email"})
    assert schema_1 == schema_2 == schema_3
