import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openapi-schema-pydantic-v2",
    version="0.0.1",
    author="0xsirsaif",
    description="OpenAPI (v3) specification schema as pydantic V2 class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xsirsaif/openapi-schema-pydantic2",
    packages=setuptools.find_packages(exclude=["tests"]),
    package_data={"openapi_schema_pydantic2": ["py.typed"]},
    install_requires=["pydantic>=2.6.0"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6.1",
)
