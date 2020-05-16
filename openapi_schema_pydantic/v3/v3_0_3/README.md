# OpenAPI v3.0.3 schema classes

## Alias

Due to the reserved words in python and pydantic,
the following fields are used with [alias](https://pydantic-docs.helpmanual.io/usage/schema/#field-customisation) feature provided by pydantic:

| Class | Field name in the class | Alias (as in OpenAPI spec) |
| ----- | ----------------------- | -------------------------- |
| Header | param_in | in |
| MediaType | media_type_schema | schema |
| Parameter | param_in | in |
| Parameter | param_schema | schema |
| PathItem | ref | $ref |
| Reference | ref | $ref |
| SecurityScheme | security_scheme_in | in |

> For convenience of object creation, the classes mentioned in above
> has configured `allow_population_by_field_name=True`.
>
> Reference: [Pydantic's Model Config](https://pydantic-docs.helpmanual.io/usage/model_config/)