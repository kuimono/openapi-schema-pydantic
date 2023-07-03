import logging
from typing import Any, List, Set, Type

from pydantic import BaseModel
from pydantic.json_schema import models_json_schema, JsonSchemaMode

from . import Components, OpenAPI, Reference, Schema

logger = logging.getLogger(__name__)

PydanticType = BaseModel
ref_prefix = "#/components/schemas/"
ref_template = ref_prefix + "{model}"


class PydanticSchema(Schema):
    """Special `Schema` class to indicate a reference from pydantic class"""

    schema_class: Type[BaseModel]
    """the class that is used for generate the schema"""


def get_mode(cls: Type[BaseModel], default: JsonSchemaMode = "validation") -> JsonSchemaMode:
    if not hasattr(cls, "model_config"):
        return default
    return cls.model_config.get("json_schema_mode", default)


def construct_open_api_with_schema_class(
    open_api: OpenAPI,
    schema_classes: List[Type[BaseModel]] | None = None,
    scan_for_pydantic_schema_reference: bool = True,
    by_alias: bool = True,
) -> OpenAPI:
    """
    Construct a new OpenAPI object, with the use of pydantic classes to produce JSON schemas

    :param open_api: the base `OpenAPI` object
    :param schema_classes: pydanitic classes that their schema will be used "#/components/schemas" values
    :param scan_for_pydantic_schema_reference: flag to indicate if scanning for `PydanticSchemaReference` class
                                               is needed for "#/components/schemas" value updates
    :param by_alias: construct schema by alias (default is True)
    :return: new OpenAPI object with "#/components/schemas" values updated.
             If there is no update in "#/components/schemas" values, the original `open_api` will be returned.
    """
    new_open_api: OpenAPI = open_api.model_copy(deep=True)
    if scan_for_pydantic_schema_reference:
        extracted_schema_classes = _handle_pydantic_schema(new_open_api)
        if schema_classes:
            schema_classes = list({*schema_classes, *_handle_pydantic_schema(new_open_api)})
        else:
            schema_classes = extracted_schema_classes

    if not schema_classes:
        return open_api

    schema_classes.sort(key=lambda x: x.__name__)
    logger.debug(f"schema_classes{schema_classes}")

    # update new_open_api with new #/components/schemas
    # Note: the mode (validation or serialization) affects
    # optional and computed fields.
    key_map, schema_definitions = models_json_schema(
        [(c, get_mode(c)) for c in schema_classes],
        by_alias=by_alias,
        ref_template=ref_template,
    )
    if not new_open_api.components:
        new_open_api.components = Components()
    if new_open_api.components.schemas:
        for existing_key in new_open_api.components.schemas:
            if existing_key in schema_definitions["$defs"]:
                logger.warning(
                    f'"{existing_key}" already exists in {ref_prefix}. '
                    f'The value of "{ref_prefix}{existing_key}" will be overwritten.'
                )
        new_open_api.components.schemas.update(
            {key: Schema.model_validate(schema_dict) for key, schema_dict in schema_definitions["$defs"].items()}
        )
    else:
        new_open_api.components.schemas = {
            key: Schema.model_validate(schema_dict) for key, schema_dict in schema_definitions["$defs"].items()
        }
    return new_open_api


def _handle_pydantic_schema(open_api: OpenAPI) -> List[Type[BaseModel]]:
    """
    This function traverses the `OpenAPI` object and

    1. Replaces the `PydanticSchema` object with `Reference` object, with correct ref value;
    2. Extracts the involved schema class from `PydanticSchema` object.

    **This function will mutate the input `OpenAPI` object.**

    :param open_api: the `OpenAPI` object to be traversed and mutated
    :return: a list of schema classes extracted from `PydanticSchema` objects
    """

    pydantic_types: Set[Type[BaseModel]] = set()

    def _traverse(obj: Any):
        if isinstance(obj, BaseModel):
            fields = obj.model_fields_set
            for field in fields:
                child_obj = obj.__getattribute__(field)
                if isinstance(child_obj, PydanticSchema):
                    logger.debug(f"PydanticSchema found in {obj.__repr_name__()}: {child_obj}")
                    obj.__setattr__(field, _construct_ref_obj(child_obj))
                    pydantic_types.add(child_obj.schema_class)
                else:
                    _traverse(child_obj)
        elif isinstance(obj, list):
            for index, elem in enumerate(obj):
                if isinstance(elem, PydanticSchema):
                    logger.debug(f"PydanticSchema found in list: {elem}")
                    obj[index] = _construct_ref_obj(elem)
                    pydantic_types.add(elem.schema_class)
                else:
                    _traverse(elem)
        elif isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, PydanticSchema):
                    logger.debug(f"PydanticSchema found in dict: {value}")
                    obj[key] = _construct_ref_obj(value)
                    pydantic_types.add(value.schema_class)
                else:
                    _traverse(value)

    _traverse(open_api)
    return list(pydantic_types)


def _construct_ref_obj(pydantic_schema: PydanticSchema):
    ref_obj = Reference(ref=ref_prefix + pydantic_schema.schema_class.__name__)
    logger.debug(f"ref_obj={ref_obj}")
    return ref_obj
