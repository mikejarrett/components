# -*- coding: utf-8 -*-
import argparse
import os
import sys

try:
    raw_input = raw_input
except:
    raw_input = input

from component_generator import ComponentGenerator, ENCODING, BLANK_LINE, FROM_IMPORT_TEMPLATE


# component_name/
#   logic/
#       __init__.py
#       logic.py
#       tests/
#           __init__.py
#           interface.py
#           tests.py

def validate_component_name(component_name):
    if component_name[0].isdigit():
        msg = "Component name '{0}' cannot start with a digit.".format(
            component_name
        )
        print(msg, file=sys.stderr)
        sys.exit(1)

    words = [words.title() for words in component_name.split(' ')]
    return '_'.join(words)


def create_directory_structure(component_name):
    print('Creating directory structure...')
    lower_component_name = component_name.lower()

    base_path = './{}'.format(lower_component_name)
    # Logic
    path = '{}/logic/tests'.format(base_path)
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    create_file('{}/__init__.py'.format(path), ENCODING)

    create_file('{}/logic/__init__.py'.format(base_path), ENCODING)

    # Storage
    path = '{}/storage/tests'.format(base_path)
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    create_file('{}/__init__.py'.format(path), ENCODING)

    create_file('{}/storage/__init__.py'.format(base_path), ENCODING)

    # Clients
    path = '{}/clients/tests'.format(base_path)
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    create_file('{}/__init__.py'.format(path), ENCODING)

    create_file('{}/clients/__init__.py'.format(base_path), ENCODING)


def create_file(path, data):
    with open(path, 'w') as file_obj:
        file_obj.write(data)


def build_logic_structure(component_name, py2):
    print('Creating logic files...')
    if not os.path.exists(component_name.lower()):
        msg = 'Directory structure is not in place! Exiting'
        print(msg, file=sys.stderr)
        sys.exit(1)

    lower_component_name = component_name.lower()
    logic_class_name = '{}Logic'.format(component_name.replace('_', ''))
    logic_file_body = ''.join([
        ENCODING,
        BLANK_LINE,
        BLANK_LINE,
        ComponentGenerator.generate_class(logic_class_name, python2=py2),
        BLANK_LINE,
        ComponentGenerator.generate_method_stub(
            'create_{0}'.format(lower_component_name),
        ),
        BLANK_LINE,
        ComponentGenerator.generate_method_stub(
            'get_{0}_by_id'.format(lower_component_name),
            ['id'],
        ),
    ])

    logic_base_path = './{}/logic'.format(lower_component_name)
    create_file('{}/logic.py'.format(logic_base_path), logic_file_body)

    create_file('{}/tests/__init__.py'.format(logic_base_path), ENCODING)
    interface_body = ''.join([
        ENCODING,

    ])

    init_file_body = ''.join([
        ENCODING,
        BLANK_LINE,
        FROM_IMPORT_TEMPLATE.format(
            module_path='{}.logic'.format(lower_component_name),
            import_name=logic_class_name
        ),
    ])
    create_file('{}/__init__.py'.format(logic_base_path), init_file_body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Component Generator')
    parser.add_argument(
        'name',
        help='Name of the component to be generated.'
    )
    parser.add_argument(
        'py2',
        nargs='?',
        help='If passed in build Python 2 styled objects.'
    )

    args = parser.parse_args()

    py2 = bool(args.py2)
    component_name = args.name
    component_name = validate_component_name(component_name)

    if os.path.exists(component_name.lower()):
        print(
            'Directory structure already in place. \n'
            'Continuing could possibly -- and PROBABLY WILL -- replace all '
            'files.'
        )
        answer = raw_input('Do you want to continue? ([y]/n) ')
        if answer.lower() == 'n':
            sys.exit(0)

    create_directory_structure(component_name)
    build_logic_structure(component_name, py2)
