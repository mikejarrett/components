# -*- coding: utf-8 -*-
import argparse
import logging
import os
import sys

try:
    raw_input = input
except: # We're using Python 2
    raw_input = raw_input

from component_generator import ComponentGenerator, ENCODING

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def validate_component(component):
    if component[0].isdigit():
        msg = "Component name '{0}' cannot start with a digit.".format(
            component
        )
        logging.error(msg)
        sys.exit(1)

    words = [words.title() for words in component.split(' ')]
    return '_'.join(words)


def create_modules(component, additional_dirs=None):
    """ Create the directory structure for the new component.

    Args:
        component (str): The name of the new component.
        additional_dirs (list optional): Additional directories to be created.
    """
    logging.info('Creating directory structure...')

    lower_component = component.lower()

    if additional_dirs is None:
        additional_dirs = []

    additional_dirs = [
        os.path.join(
            lower_component,
            validate_component(additional).lower(),
            'tests'
        )
        for additional in additional_dirs
    ]

    dirs = [
        os.path.join(lower_component, 'logic', 'tests'),
        os.path.join(lower_component, 'storage', 'tests'),
        os.path.join(lower_component, 'clients', 'tests'),
    ] + additional_dirs

    # Create the directory structure.
    # If the dir already exists. Just skip over it.
    for path in dirs:
        if os.path.exists(path):
            continue
        else:
            os.makedirs(path)

    def create_init_files(root_dir):
        for dir_name, subdir_list, file_list in os.walk(root_dir):
            filepath = os.path.join(dir_name, '__init__.py')
            create_file(filepath, init_file_body)
            for sub_dir in subdir_list:
                new_path = os.path.join(dir_name, sub_dir)
                create_init_files(new_path)

    root_dir = os.path.join(os.curdir, lower_component)
    init_file_body = ComponentGenerator.build_file_body({'__init__': True})
    create_init_files(root_dir)


def create_file(path, data):
    with open(path, 'w') as file_obj:
        file_obj.write(data)


def build_logic_structure(component, py2=False):
    logging.info('Creating logic files...')

    lower_component = component.lower()
    module_path = os.path.join(lower_component, 'logic')

    component_class = component.replace('_', '')
    logic_class_name = '{0}Logic'.format(component_class)

    data = {
        'class_name': logic_class_name,
        'python2': py2,
        'methods': [{
            'name': '__init__'.format(lower_component),
        }, {
            'name': 'create_{0}'.format(lower_component),
        }, {
            'name': 'get_{0}_by_id'.format(lower_component),
            'args': ['id'],
        }]
    }
    create_file(
        os.path.join(module_path, 'logic.py'),
        ComponentGenerator.build_file_body(data)
    )

    test_interface = '{0}Interface'.format(logic_class_name)
    storage_name = '{0}PureMemoryStorage'.format(component_class)
    data = {
        'class_name': test_interface,
        'python2': py2,
        'methods': [
            {
                'name': 'test_create_{0}'.format(lower_component),
                'additional': [
                    "{0}raise NotImplementedError"
                    "('You must write this test!')".format(' ' * 8),
                ]
            }, {
                'name': 'test_get_{0}_by_id'.format(lower_component),
                'additional': [
                    "{0}raise NotImplementedError"
                    "('You must write this test!')".format(' ' * 8),
                ]
            }
        ]
    }
    create_file(
        os.path.join(module_path, 'tests', 'interface.py'),
        ComponentGenerator.build_file_body(data)
    )

    test_class_name = 'Test{0}'.format(logic_class_name)
    data = {
        'class_name': test_class_name,
        'python2': py2,
        'class_inheritance': [test_interface, 'TestCase'],
        'class_level_arguments': [
            '{0}storage = {1}()'.format(' ' * 4, storage_name),
        ],
        'from_imports': [
            ['unittest', 'TestCase'],
            ['{0}.logic'.format(lower_component), logic_class_name],
            ['{0}.storage'.format(lower_component), storage_name],
            [
                '{0}.logic.tests.interface'.format(lower_component),
                test_interface
            ],
        ],
        'methods': [
            {
                'name': 'setUp',
            }, {
                'name': 'tearDown',
                'additional': [
                    '{0}self.storage.wipe()'.format(' ' * 8),
                ]
            }
        ]
    }
    create_file(
        os.path.join(module_path, 'tests', 'tests.py'),
        ComponentGenerator.build_file_body(data)
    )

    create_file(
        os.path.join(module_path, 'tests', '__init__.py'),
        ComponentGenerator.build_file_body({'__init__': True})
    )

    data = {
        'from_imports': [
            ['.logic'.format(lower_component), logic_class_name]
        ],
        '__init__': True,
    }
    create_file(
        os.path.join(module_path, '__init__.py'),
        ComponentGenerator.build_file_body(data),
    )


def build_storage_structure(component, py2=False):
    logging.info('Creating storage files...')

    lower_component = component.lower()
    module_path = os.path.join(lower_component, 'storage')

    component_class = component.replace('_', '')
    storage_class_name = '{0}PureMemoryStorage'.format(component_class)

    data = {
        'class_name': storage_class_name,
        'python2': py2,
        'methods': [{
            'name': '__init__'.format(lower_component),
            'additional': [
                '{0}self.storage = []'.format(' ' * 8),
            ],
        }, {
            'name': 'wipe',
            'additional': [
                '{0}self.storage = []'.format(' ' * 8),
            ],
        }, {
            'name': 'persist_{0}'.format(lower_component),
        }, {
            'name': 'retrieve_{0}_by_id'.format(lower_component),
            'args': ['id'],
        }]
    }
    create_file(
        os.path.join(module_path, 'pure_memory.py'),
        ComponentGenerator.build_file_body(data)
    )

    test_interface = '{0}Interface'.format(storage_class_name)
    storage_name = '{0}PureMemoryStorage'.format(component_class)
    data = {
        'class_name': test_interface,
        'python2': py2,
        'methods': [
            {
                'name': 'test_persist_{0}'.format(lower_component),
                'additional': [
                    "{0}raise NotImplementedError"
                    "('You must write this test!')".format(' ' * 8),
                ]
            }, {
                'name': 'test_retrieve_{0}_by_id'.format(lower_component),
                'additional': [
                    "{0}raise NotImplementedError"
                    "('You must write this test!')".format(' ' * 8),
                ]
            }
        ]
    }
    create_file(
        os.path.join(module_path, 'tests', 'interface.py'),
        ComponentGenerator.build_file_body(data)
    )

    test_class_name = 'Test{0}'.format(storage_class_name)
    data = {
        'class_name': test_class_name,
        'python2': py2,
        'class_inheritance': [test_interface, 'TestCase'],
        'class_level_arguments': [
            '{0}storage = {1}()'.format(' ' * 4, storage_name),
        ],
        'from_imports': [
            ['unittest', 'TestCase'],
            ['{0}.storage'.format(lower_component), storage_name],
            [
                '{0}.storage.tests.interface'.format(lower_component),
                test_interface
            ],
        ],
        'methods': [
            {
                'name': 'setUp',
            }, {
                'name': 'tearDown',
                'additional': [
                    '{0}self.storage.wipe()'.format(' ' * 8),
                ]
            }
        ]
    }
    create_file(
        os.path.join(module_path, 'tests', 'tests.py'),
        ComponentGenerator.build_file_body(data)
    )

    create_file(
        os.path.join(module_path, 'tests', '__init__.py'),
        ComponentGenerator.build_file_body({'__init__': True})
    )

    data = {
        'from_imports': [
            [
                '{0}.storage.pure_memory'.format(lower_component),
                storage_class_name
            ]
        ],
        '__init__': True,
    }
    create_file(
        os.path.join(module_path, '__init__.py'),
        ComponentGenerator.build_file_body(data),
    )


def build_client_structure(component, py2=False):
    logging.info('Creating client files...')

    lower_component = component.lower()
    module_path = os.path.join(lower_component, 'clients')

    component_class = component.replace('_', '')
    client_class_name = '{0}FakeClient'.format(component_class)

    data = {
        'class_name': client_class_name,
        'python2': py2,
        'methods': [{
            'name': '__init__'.format(lower_component),
        }, {
            'name': 'create_{0}'.format(lower_component),
        }, {
            'name': 'get_{0}_by_id'.format(lower_component),
            'args': ['id'],
        }]
    }
    create_file(
        os.path.join(module_path, 'fake.py'),
        ComponentGenerator.build_file_body(data)
    )

    test_interface = '{0}Interface'.format(client_class_name)
    client_name = '{0}FakeClient'.format(component_class)
    data = {
        'class_name': test_interface,
        'python2': py2,
        'methods': [
            {
                'name': 'test_create_{0}'.format(lower_component),
                'additional': [
                    "{0}raise NotImplementedError"
                    "('You must write this test!')".format(' ' * 8),
                ]
            }, {
                'name': 'test_get_{0}_by_id'.format(lower_component),
                'additional': [
                    "{0}raise NotImplementedError"
                    "('You must write this test!')".format(' ' * 8),
                ]
            }
        ]
    }
    create_file(
        os.path.join(module_path, 'tests', 'interface.py'),
        ComponentGenerator.build_file_body(data)
    )

    test_class_name = 'Test{0}'.format(client_class_name)
    data = {
        'class_name': test_class_name,
        'python2': py2,
        'class_inheritance': [test_interface, 'TestCase'],
        'class_level_arguments': [
            '{0}client = {1}()'.format(' ' * 4, client_name),
        ],
        'from_imports': [
            ['unittest', 'TestCase'],
            ['{0}.clients'.format(lower_component), client_name],
            [
                '{0}.clients.tests.interface'.format(lower_component),
                test_interface
            ],
        ],
        'methods': [
            {
                'name': 'setUp',
            }, {
                'name': 'tearDown',
            }
        ]
    }
    create_file(
        os.path.join(module_path, 'tests', 'tests.py'),
        ComponentGenerator.build_file_body(data)
    )

    create_file(
        os.path.join(module_path, 'tests', '__init__.py'),
        ComponentGenerator.build_file_body({'__init__': True})
    )

    data = {
        'from_imports': [
            ['{0}.clients.fake'.format(lower_component), client_class_name]
        ],
        '__init__': True,
    }
    create_file(
        os.path.join(module_path, '__init__.py'),
        ComponentGenerator.build_file_body(data),
    )
