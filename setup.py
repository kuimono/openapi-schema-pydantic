import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openapi-schema-pydantic",
    version="0.3.0",
    author="Kuimono",
    description="OpenAPI (v3) specification schema as pydantic class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuimono/openapi-schema-pydantic",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=["pydantic==1.5.1"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
