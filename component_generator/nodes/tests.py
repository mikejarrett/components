# -*- coding: utf-8 -*-
from unittest import TestCase
from os.path import join
import os

from component_generator import constants
from component_generator.nodes import *
from component_generator import processors

class Test(TestCase):

    maxDiff = None

    kwargs = {
        'storage_prefix_mapping': constants.STORAGE_PREFIX_MAPPING,
        'logic_arguments': {},
        'logic_kwarguments': {},
        'storage_arguments': {},
        'storage_kwarguments': {},
        'name_titled': ['Foo'],
        'name_underscored_lowered': ['foo'],
        'path': join('blah'),
        'logic_prefix_mapping': constants.LOGIC_PREFIX_MAPPING,
    }

    def test_file_path_generation(self):
        config = ComponentGenerator(**self.kwargs).config
        # actual = processors.build_init_files_for_config(config)

        expected = sorted([
            # join('blah', 'component', '__init__.py'),
            join('blah', 'component', 'client', '__init__.py'),
            join('blah', 'component', 'client', 'foo.py'),
            join('blah', 'component', 'logic', '__init__.py'),
            join('blah', 'component', 'logic', 'foo.py'),
            join('blah', 'component', 'storage', '__init__.py'),
            join('blah', 'component', 'storage', 'foo.py'),
            # join('blah', 'component', 'tests', '__init__.py'),
            # join('blah', 'component', 'tests', 'client', '__init__.py'),
            join('blah', 'component', 'tests', 'client', 'test_foo.py'),
            # join('blah', 'component', 'tests', 'logic', '__init__.py'),
            join('blah', 'component', 'tests', 'logic', 'test_foo.py'),
            # join('blah', 'component', 'tests', 'storage', '__init__.py'),
            join('blah', 'component', 'tests', 'storage', 'test_foo.py'),
        ])
        self.assertEqual(sorted(list(config.keys())), expected)

