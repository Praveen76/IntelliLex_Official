#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'intlx_model'
DESCRIPTION = "Intellilex model for GenAI package"
EMAIL = "panwla@ur.rochester.edu"
AUTHOR = "Praveen Kumar Anwla"
REQUIRES_PYTHON = ">=3.10.0"
long_description = DESCRIPTION

# Setting up directories
ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'  # Update as necessary
PACKAGE_DIR = ROOT_DIR / 'intlx_model'  # Points to your package directory

# Load the VERSION file
about = {}
with open(PACKAGE_DIR / "VERSION") as f:
    about["__version__"] = f.read().strip()

# Read requirements file
def list_reqs(fname="requirements.txt"):
    with open(REQUIREMENTS_DIR / fname) as fd:
        return fd.read().splitlines()

# Setup configuration
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(where=ROOT_DIR, exclude=("tests",)),
    package_data={
        'intlx_model': ['VERSION', "db/*"]  # Ensure this reflects actual internal structure
    },
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license="BSD-3",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
