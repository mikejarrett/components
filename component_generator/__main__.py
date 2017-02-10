#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=redefined-builtin,invalid-name
import sys

from component_generator.arg_parser import parse_args
from component_generator.generator import ComponentGenerator
from component_generator.logger import set_log_level_to_debug
from component_generator.utils import clean_raw_name
from component_generator.writer import write_config


try:
    input = raw_input
except NameError:  # Python 3
    pass


def main(args=None):  # pragma: no cover
    if args is None:
        args = sys.argv[1:]
    if not args:
        args = ['--help']

    args = parse_args(args)

    verbose = args.verbose
    if verbose:
        set_log_level_to_debug()

    names = clean_raw_name('_'.join(args.component_name))

    component_generator = ComponentGenerator(
        name_titled=names.titled,
        name_underscored_lowered=names.underscored_lower
    )

    write_config(component_generator.config)


if __name__ == '__main__':
    main()
