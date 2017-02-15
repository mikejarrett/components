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
"""
from . import templates, constants
from .generator import Generator as Combiner


######
# component_loader bar foo


# # Build bar
# persist_method = Method(persist_{0})

# klass = Klass(Bar)
# klass.add_method(persist_method)

# bar_module = Module(bar)  # bar.py
# bar_module.add_class(klass)

# bar_package = Package(pure_memory)
# bar_package.add_module(bar_module)

# # Build foo
# persist_method = Method(persist_{0})

# klass = Klass(foo)
# klass.add_method(persist_method)

# foo_module = Module(foo)  # foo.py
# foo_module.add_class(klass)

# foo_package = Package(pure_memory)
# foo_package.add_module(foo_module)

# storage_package = Package(storage)
# storage_package.add_subpackage(bar_package)
# storage_package.add_subpackage(foo_package)

# component_package = Package(component)
# component_package.add_subpackage(storage_package)
