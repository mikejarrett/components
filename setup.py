#!/usr/bin/env python
from distutils.core import setup

import src

setup(
    name='component-generator',
    version=src.__version__,
    description='Stub out components.',
    author='Mike Jarrett',
    author_email='',
    url='',
    package_dir={
        'component_generator': 'src',
    },
    packages=['component_generator'],
    entry_points={
        'console_scripts': [
            'startcomponent = component_generator.__main__:main',
        ],
    },
)
