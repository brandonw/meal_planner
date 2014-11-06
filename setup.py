# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import meal_planner
version = meal_planner.__version__

setup(
    name='Meal Planner',
    version=version,
    author='',
    author_email='brandon.waskiewicz@gmail.com',
    packages=[
        'meal_planner',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.1',
    ],
    zip_safe=False,
    scripts=['meal_planner/manage.py'],
)