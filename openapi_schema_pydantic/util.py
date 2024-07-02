import logging
from typing import Any, List, Set, Type, TypeVar, Optional

from pydantic import BaseModel

from . import Components, OpenAPI, Reference, Schema

logger = logging.getLogger(__name__)

PydanticType = TypeVar("PydanticType", bound=BaseModel)
ref_prefix = "#/components/schemas/"


class PydanticSchema(Schema):
    """Special `Schema` class to indicate a reference from pydantic class"""

    schema_class: Type[PydanticType] = ...
    """the class that is used for generate the schema"""


def construct_open_api_with_schema_class(
    open_api: OpenAPI,
    schema_classes: Optional[List[Type[BaseModel]]] = None,
    scan_for_pydantic_schema_reference: bool = True,
    by_alias: bool = True,
    ref_prefix: str = "#/components/schemas/",
) -> OpenAPI:
    """
    Construct a new OpenAPI object, using Pydantic classes to produce JSON schemas.

    :param open_api: the base `OpenAPI` object
    :param schema_classes: list of Pydantic classes whose schemas will be used in "#/components/schemas"
    :param scan_for_pydantic_schema_reference: flag to indicate if scanning for additional schema references is needed
    :param by_alias: whether to construct schema by alias (default is True)
    :param ref_prefix: reference prefix for schema IDs
    :return: new OpenAPI object with updated "#/components/schemas".
    """
    new_open_api: OpenAPI = open_api.model_copy(deep=True)
    components_schemas = {}

    if scan_for_pydantic_schema_reference:
        # Suppose _handle_pydantic_schema is a function to extract Pydantic classes from new_open_api
        extracted_schema_classes = _handle_pydantic_schema(new_open_api)
        schema_classes = list(set(schema_classes or []) | set(extracted_schema_classes))

    if not schema_classes:
        return open_api

    # Sort classes by name for consistent ordering
    schema_classes.sort(key=lambda x: x.__name__)

    # Generate schema for each class and update the OpenAPI components
    for cls in schema_classes:
        schema = cls.model_json_schema(by_alias=by_alias)
        definition_name = cls.__name__
        components_schemas[definition_name] = Schema.model_validate(schema)

    if not new_open_api.components:
        new_open_api.components = Components()

    if new_open_api.components.schemas:
        for key, value in components_schemas.items():
            if key in new_open_api.components.schemas:
                logger.warning(
                    f'"{key}" already exists in {ref_prefix}. '
                    f'The value of "{ref_prefix}{key}" will be overwritten.'
                )
        new_open_api.components.schemas.update(components_schemas)
    else:
        new_open_api.components.schemas = components_schemas

    return new_open_api


def _handle_pydantic_schema(open_api: OpenAPI) -> List[Type[PydanticType]]:
    """
    This function traverses the `OpenAPI` object and

    1. Replaces the `PydanticSchema` object with `Reference` object, with correct ref value;
    2. Extracts the involved schema class from `PydanticSchema` object.

    **This function will mutate the input `OpenAPI` object.**

    :param open_api: the `OpenAPI` object to be traversed and mutated
    :return: a list of schema classes extracted from `PydanticSchema` objects
    """

    pydantic_types: Set[Type[PydanticType]] = set()

    def _traverse(obj: Any):
        if isinstance(obj, BaseModel):
            fields = obj.model_fields_set
            for field in fields:
                child_obj = obj.__getattribute__(field)
                if isinstance(child_obj, PydanticSchema):
                    logger.debug(
                        f"PydanticSchema found in {obj.__repr_name__()}: {child_obj}"
                    )
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
