# Change Log

## v1.2.0 - Unreleased

### Added
- Support OpenAPI schema v3.1.0


## v1.1.0 - 2020-05-28

### Added
- Add `by_alias` parameter in `util.construct_open_api_with_schema_class` function, to allow construct JSON schema by alias


## v1.0.0 - 2020-05-26

Official release


## v0.3.0 - 2020-05-22

## Updated
- Use `extra = Extra.forbid` config, so the schema classes does not support 
  [Specification Extensions](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#specificationExtensions)
  in general.
    - If an extension field (e.g. `x-examples` in `Schema`) is needed,
      one may create a child class to specify the addition field (with correct typing and properties).


## v0.2.2 - 2020-05-18

### Fixed
- Fixed issue of `Refeence` type incorrectly parsed in `Schema` object (due to incorrect union field order)
    - [Reference: pydantic Union type](https://pydantic-docs.helpmanual.io/usage/types/#unions)


## v0.2.1 - 2020-05-18

### Updated
- Remove `extra = Extra.allow` config, so the schema classes does not support 
  [Specification Extensions](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#specificationExtensions)
  in general.
    - If an extension field (e.g. `x-examples` in `Schema`) is needed,
      one may create a child class to specify the addition field (with correct typing and properties).


## v0.2.0 - 2020-05-17

### Added
- Added field definitions of `Schema` class
- Added config `extra = Extra.allow` to schema types to allow
  [Specification Extensions](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#specificationExtensions)
- Added test cases on field alias

### Updated
- Updated README.md
- Minor code formatting


## v0.1.2 - 2020-05-16

### Added
- Added documentation for alias used in the OpenAPI classes

### Updated
- Updated the config of OpenAPI classes (with alias), to use `allow_population_by_field_name=True`.

### Fixed
- Fixed `SecurityRequirement` to use correct typing (`Dict[str, List[str]]`)
- Fixed `Callback` and `SecurityRequirement`, to be a `Dict` type instead of a class


## v0.1.1 - 2020-05-16

- First Release