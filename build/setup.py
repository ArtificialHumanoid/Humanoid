from setuptools import setup

with open("../README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding='UTF-8') as fh:
    requirements = fh.read().split("\n")

setup(
    version="0.0.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[requirements],
)
