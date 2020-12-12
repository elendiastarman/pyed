#!/usr/bin/env python
from setuptools import setup

setup(
  name='Pyed',
  author='El\'endia Starman',
  license='MIT',
  description='A fundamentally graphical programming language.',
  install_requires=[
    'mypy',
    'ipdb',
  ],
  python_requires='>=3.8',
)
