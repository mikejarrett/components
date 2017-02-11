#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=redefined-builtin,invalid-name
import logging
import sys

from component_generator.arg_parser import parse_args
from component_generator.generator import ComponentGenerator
from component_generator.logger import set_log_level_to_debug
from component_generator.utils import clean_raw_name
from component_generator.writer import write_config


logger = logging.getLogger(__name__)


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
            build_storage_prefix_mapping(args.storage_types)

        logic_arguments = ComponentGenerator.build_arguments(
            args.logic_arguments,
            component_name
        )
        logic_kwarguments = ComponentGenerator.build_kwarguments(
            args.logic_kwarguments,
            component_name
        )

        storage_arguments = ComponentGenerator.build_arguments(
            args.storage_arguments,
            component_name
        )
        storage_kwarguments = ComponentGenerator.build_kwarguments(
            args.storage_kwarguments,
            component_name
        )

        try:
            component_generator = ComponentGenerator(
                name_titled=names.titled,
                name_underscored_lowered=names.underscored_lower,
                storage_prefix_mapping=storage_prefix_mapping,
                logic_arguments=logic_arguments,
                logic_kwarguments=logic_kwarguments,
                storage_arguments=storage_arguments,
                storage_kwarguments=storage_kwarguments,
            )
            config.update(component_generator.config)

        except TypeError as err:
            logger.warning(
                'Problem generating %s: %s',
                component_name,
                str(err)
            )

    config = ComponentGenerator.build_init_files_for_config(config)
    write_config(config)


if __name__ == '__main__':
    main()
