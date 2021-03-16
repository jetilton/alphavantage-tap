#!/usr/bin/env python
from setuptools import setup

setup(
    name="alphavantage-tap",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["av-tap"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    alphavantage-tap=av-tap:main
    """,
    packages=["av-tap"],
    package_data = {
        "schemas": ["av-tap/schemas/*.json"]
    },
    include_package_data=True,
)
