from openapi_pydantic.v3.v3_0_3 import (
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


def test_config_example() -> None:
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


def _assert_config_examples(schema_type: object) -> None:
    Config = getattr(schema_type, "Config", None)
    schema_extra = getattr(Config, "schema_extra", None)
    if schema_extra is not None:
        examples = schema_extra.get("examples")
        for example_dict in examples:
            obj = schema_type(**example_dict)  # type: ignore[operator]
            assert obj.__fields_set__
