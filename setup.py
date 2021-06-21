#!/usr/bin/env python

import sys
from os import path

from setuptools import setup, find_packages


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


install_requires = []


# Require python 3.7
if sys.version_info.major != 3 and sys.version_info.minor < 7:
    sys.exit("'nullsafe' requires Python >= 3.7!")


setup(
    name="nullsafe",
    version="0.2.1",
    author="Paaksing",
    author_email="paaksingtech@gmail.com",
    url="https://github.com/paaksing/nullsafe-python",
    description="Null safe support for Python",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["null-safe", "nullsafe", "none aware", "python"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    license="MIT",
    packages=find_packages(exclude=("test")),
    zip_safe=True,
    install_requires=install_requires,
    include_package_data=True,
)
