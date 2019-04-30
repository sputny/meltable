#!/usr/bin/env python3
# coding=<utf-8>
from setuptools import setup, find_packages


setup(
    name="meltable",
    version="0.1",
    packages=find_packages(),
    install_requires=['PyPDF2', 'docopt'],
    author="thuttner",
    license="GPL2",
    entry_points={
        'console_scripts': [
            'meltable = meltable.meltable:main',
            ]
        },
    )
