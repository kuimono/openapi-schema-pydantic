# Change Log

## v0.1.2 - Unreleased

### Added
- Added documentation for alias used in the OpenAPI classes

### Updated
- Updated the config of OpenAPI classes (with alias), to use `allow_population_by_field_name=True`.

### Fixed
- Fixed `SecurityRequirement` to use correct typing (`Dict[str, List[str]]`)
- Fixed `Callback` and `SecurityRequirement`, to be a `Dict` type instead of a class


## v0.1.1 - 2020-06-15

- First Release