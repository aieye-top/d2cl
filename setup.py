#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def get_version() -> str:
    # https://packaging.python.org/guides/single-sourcing-package-version/
    init = open(os.path.join("d2cl", "__init__.py"), "r").read().split()
    return init[init.index("__version__") + 2][1:-1]


setup(
    name="aieye",
    version=get_version(),
    description="A Library for cheap deep Learning",
    author="StevenJokess",
    author_email="llgg8679@qq.com",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(
        exclude=["examples", "examples.*"]
    ),
    install_requires=[
        "torch>=1.6.0"
    ],
    extras_require={
        "dev": [
            "flake8",
            "mypy",
            "d2lbook",
            "sphinxcontrib-bibtex==1.0.0",
        ],
    },
)
