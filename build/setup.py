import os

from setuptools import setup
from setuptools.config import expand

if __debug__:
    print(os.getcwd())

with open("../README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="UTF-8'") as fh:
    requirements = fh.read().split("\n")

# Monkey patch.


def _assert_local(_, __):
    return True


expand._assert_local = _assert_local


setup(
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[requirements],
)
