# -*- coding: utf-8 -*-
import argparse
import logging
import os
import sys

try:
    input = raw_input
except NameError:  # We're in Python 3
    pass

from .structure import (
    build_client_structure,
    build_logic_structure,
    build_storage_structure,
    create_modules,
    validate_component,
)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(description='Component Generator')
    parser.add_argument(
        'name',
        help='Name of the component to be generated.'
    )
    parser.add_argument(
        '--py2',
        nargs='?',
        help='If passed in build Python 2 styled objects.'
    )

    parser.add_argument(
        '-a',
        '--additional',
        nargs='*',
        help=(
            'Additional modules to create. Using this command will create '
            'additional modules and tests submodules. All will be empty '
            'except for __init__.py files.'
        ),
    )

    args = parser.parse_args()

    py2 = bool(args.py2)
    component = args.name
    component = validate_component(component)

    if os.path.exists(component.lower()):
        print(
            'Directory structure already in place. \n'
            'Continuing could possibly -- and PROBABLY WILL -- replace all '
            'files.'
        )
        answer = input('Do you want to continue? ([y]/n) ')
        if answer.lower() == 'n':
            sys.exit(0)

    create_modules(component, args.additional)
    build_logic_structure(component, py2)
    build_storage_structure(component, py2)
    build_client_structure(component, py2)


if __name__ == '__main__':
    main()
