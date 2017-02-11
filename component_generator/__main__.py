#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=redefined-builtin,invalid-name
import os
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

    config = {}
    for component_name in args.component_names:
        names = clean_raw_name(component_name)

        storage_prefix_mapping = ComponentGenerator. \
            build_storage_prefix_mapping(args.storage)

        component_generator = ComponentGenerator(
            name_titled=names.titled,
            name_underscored_lowered=names.underscored_lower,
            storage_prefix_mapping=storage_prefix_mapping,
        )
        config.update(component_generator.config)

    config = ComponentGenerator.build_init_files_for_config(config)
    write_config(config)


if __name__ == '__main__':
    main()
