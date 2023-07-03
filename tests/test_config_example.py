from openapi_schema_pydantic import (
    OpenAPI,
    Info,
    Contact,
    License,
    Server,
    ServerVariable,
    Components,
    Paths,
    PathItem,
    Operation,
    ExternalDocumentation,
    Parameter,
    RequestBody,
    MediaType,
    Encoding,
    Responses,
    Response,
    Callback,
    Example,
    Link,
    Header,
    Tag,
    Reference,
    Schema,
    Discriminator,
    XML,
    SecurityScheme,
    OAuthFlows,
    OAuthFlow,
    SecurityRequirement,
)


def test_config_example():
    all_types = [
        OpenAPI,
        Info,
        Contact,
        License,
        Server,
        ServerVariable,
        Components,
        Paths,
        PathItem,
        Operation,
        ExternalDocumentation,
        Parameter,
        RequestBody,
        MediaType,
        Encoding,
        Responses,
        Response,
        Callback,
        Example,
        Link,
        Header,
        Tag,
        Reference,
        Schema,
        Discriminator,
        XML,
        SecurityScheme,
        OAuthFlows,
        OAuthFlow,
        SecurityRequirement,
    ]
    for schema_type in all_types:
        _assert_config_examples(schema_type)


def _assert_config_examples(schema_type):
    if not hasattr(schema_type, "model_config"):
        return
    extra = schema_type.model_config.get("json_schema_extra")
    if extra is not None:
        examples = extra.get("examples")
        for example_dict in examples:
            obj = schema_type.model_validate(example_dict)
            assert obj.model_fields_set
