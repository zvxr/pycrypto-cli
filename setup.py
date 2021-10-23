#!/usr/bin/env python

import crypto

from setuptools import setup, find_packages
from distutils.core import Extension


dependencies = ['pycrypto']

setup(
    name="pycrypto-cli",
    version=crypto.__version__,
    author="Mike McConnell",
    author_email="djrahl84@gmail.com",
    description=((
        "CLI Pycrypto wrapper: allows quick and easy implementation of " +
        "ciphers, Hashes and Keys."
    )),
    #ext_modules=[
    #    Extension(
    #        "crypto.ports._XOR",
    #        include_dirs=['crypto/ports/'],
    #        sources=["crypto/ports/XOR.c"]
    #    ),
    #],
    url="https://github.com/zvxr/pycrypto-cli",
    packages=find_packages(),
)
