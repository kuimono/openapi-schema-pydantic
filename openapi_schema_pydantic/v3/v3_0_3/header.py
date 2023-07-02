from pydantic import ConfigDict, Field
from typing import Literal

from .parameter import Parameter


class Header(Parameter):
    """
    The Header Object follows the structure of the [Parameter Object](#parameterObject) with the following changes:

    1. `name` MUST NOT be specified, it is given in the corresponding `headers` map.
    2. `in` MUST NOT be specified, it is implicitly in `header`.
    3. All traits that are affected by the location MUST be applicable to a location of `header`
       (for example, [`style`](#parameterStyle)).
    """

    name: Literal[""] = Field(default="")
    param_in: Literal["header"] = Field(default="header", alias="in")

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {"description": "The number of allowed requests in the current period", "schema": {"type": "integer"}}
            ]
        },
    )
