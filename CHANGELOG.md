# Change Log

## v0.1.3 - Unreleased

### Added
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