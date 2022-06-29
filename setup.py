import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openapi-schema-pydantic",
    version="1.2.4",
    author="Kuimono",
    description="OpenAPI (v3) specification schema as pydantic class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuimono/openapi-schema-pydantic",
    packages=setuptools.find_packages(exclude=["tests"]),
    package_data={"openapi_schema_pydantic": ["py.typed"]},
    install_requires=["pydantic>=1.8.2"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6.1",
)
