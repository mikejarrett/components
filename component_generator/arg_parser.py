# -*- coding: utf-8 -*-
import argparse


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Reduce the boiler plate when writting components.',
    )

    parser.add_argument('component_names', nargs='*')
    parser.add_argument(
        '-t',
        '--storage-types',
        nargs='*',
        default=['pure_memory'],
        help='A list of storage types to generate.',
    )
    parser.add_argument(
        '-a',
        '--logic-arguments',
        nargs='?',
        default='{}',
        help='Add additional logic methods and arguments',
    )
    parser.add_argument(
        '-k',
        '--logic-kwarguments',
        nargs='?',
        default='{}',
        help='Add additional logic methods and kwarguments',
    )
    # parser.add_argument(
    #     '-l',
    #     '--logic-methods',
    #     nargs='?',
    #     default='{}',
    #     help='Add additional logic methods',
    # )
    parser.add_argument(
        '-r',
        '--storage-arguments',
        nargs='?',
        default='{}',
        help='Add additional storage methods and arguments',
    )
    parser.add_argument(
        '-w',
        '--storage-kwarguments',
        nargs='?',
        default='{}',
        help='Add additional storage methods and kwarguments',
    )
    parser.add_argument(
        '-s',
        '--storage-methods',
        nargs='?',
        default='{}',
        help='Add additional storage methods',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Set logging level to DEBUG',
    )

    return parser.parse_args(args)
