from pydantic import BaseModel, Extra


class Schema(BaseModel):
    """
    The Schema Object allows the definition of input and output data types.
    These types can be objects, but also primitives and arrays.
    This object is an extended subset of the [JSON Schema Specification Wright Draft 00](https://json-schema.org/).

    For more information about the properties, see [JSON Schema Core](https://tools.ietf.org/html/draft-wright-json-schema-00) and [JSON Schema Validation](https://tools.ietf.org/html/draft-wright-json-schema-validation-00).
    Unless stated otherwise, the property definitions follow the JSON Schema.
    """

    # this model will not implement fields by itself;
    # instead it will rely on other BaseModel's `.dict()` function to retrieve the values.
    class Config:
        extra = Extra.allow
