# -*- coding: utf-8 -*-
import argparse


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Reduce the boiler plate when writting components.',
    )

    parser.add_argument('component_names', nargs='*')
    parser.add_argument(
        '-s',
        '--storage',
        nargs='*',
        default=['pure_memory'],
        help='A list of storage types to generate.',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Set default logging level to DEBUG',
    )

    return parser.parse_args(args)
