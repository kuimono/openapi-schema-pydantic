# Change Log

## v0.2.0 - Unreleased

### Added
- Added field definitions of `Schema` class
- Added config `extra = Extra.allow` to schema types to allow [Specification Extensions](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#specificationExtensions)
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