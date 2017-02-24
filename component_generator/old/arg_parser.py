# -*- coding: utf-8 -*-
import argparse


def parse_args(args):
    parser = argparse.ArgumentParser(
        usage='Use "component_generator --help" for more information',
        description='Reduce the boiler plate when writting components.',
    )

    parser.add_argument(
        'component_names',
        nargs='*',
        help='A list of comopents to stub out',
    )
    parser.add_argument(
        '-t',
        '--storage-types',
        default=['pure_memory'],
        metavar='str',
        nargs='*',
        help=(
            'A list of storage types to generate. A `pure_memory` storage '
            'type will always be generated. '
        ),
    )
    parser.add_argument(
        '-a',
        '--logic-arguments',
        default='{}',
        metavar='json',
        nargs='?',
        help=(
            'Extend logic and client methods by adding arguments to '
            'default methods \'{"package": {"create_{0}": ["foo"]}\' or '
            'add new methods in the same way '
            '\'{"package": {"spam": ["eggs"]}}\''
        ),
    )
    parser.add_argument(
        '-k',
        '--logic-kwarguments',
        default='{}',
        metavar='json',
        nargs='?',
        help=(
            'Extend logic and client methods by adding keyword arguments to '
            'default methods \'{"package": {"create_{0}": {"foo": null}}\' or '
            'add new methods in the same way '
            '\'{"package": {"spam": {"eggs": false}}}\''
        ),
    )
    parser.add_argument(
        '-r',
        '--storage-arguments',
        default='{}',
        metavar='json',
        nargs='?',
        help=(
            'Extend storage methods by adding arguments to default methods: '
            '\'{"package": {"create_{0}": ["foo"]}\' or add new methods in '
            'the same way: \'{"package": {"spam": ["eggs"]}}\''
        ),
    )
    parser.add_argument(
        '-w',
        '--storage-kwarguments',
        default='{}',
        metavar='json',
        nargs='?',
        help=(
            'Extend logic and client methods by adding keyword arguments to '
            'default methods \'{"package": {"create_{0}": {"foo": null}}\' or '
            'add new methods in the same way '
            '\'{"package": {"spam": {"eggs": false}}}\''
        ),
    )
    parser.add_argument(
        '-p',
        '--path',
        default=None,
        nargs='?',
        help='Where to generate the component.',
    )
    parser.add_argument(
        '-c',
        '--config',
        default=None,
        nargs='?',
        help='Path the a configuration to use.',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Set logging level to DEBUG',
    )

    return parser.parse_args(args)
