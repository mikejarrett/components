# -*- coding: utf-8 -*-
""" Usage:

    from nodes import *
    from collections import namedtuple

    Names = namedtuple('Names', ['titled', 'name_underscored_lowered'])

    kwargs = {
        'names': [Names('Foo', 'foo'), Names('Bar', 'bar')],
        'logic_prefix_mapping': {
            'logic': ['create_{0}'],
            'client': ['create_{0}']
        },
        'storage_prefix_mapping': {'storage': ['persist_{0}']},
        'storage_types': ['pure_memory', 'django'],
    }

    package = Combiner(**kwargs).build()
    package.print_file_structure()

    blah/
        __init__.py
        client/
            bar.py
            foo.py
        tests/
            __init__.py
            client/
                bar.py
                foo.py
            storage/
                bar.py
                foo.py
            logic/
                bar.py
                foo.py
        storage/
            __init__.py
            pure_memory/
                bar.py
                foo.py
            django/
                bar.py
                foo.py
        logic/
            bar.py
            foo.py


Python Usage
============

    from component_generator import *
    from component_generator.utils import clean_raw_name

    generator = Generator(
        names=[clean_raw_name('Foo Monkey'), clean_raw_name('Bar')],
        storage_types=['pure_memory', 'django'],
        additional={'bar': {'monkey': [['id'], {'blark': None}], 'spam': []}}
    )
    generator.build().print_file_structure()
    generator.print_file_structure()
"""
from . import templates, constants
from .generator import Generator
