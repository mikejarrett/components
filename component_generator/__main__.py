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
from component_generator import processors


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
    for comp_name in args.component_names:
        cleaned = processors.clean(comp_name, args)

        try:
            component_generator = ComponentGenerator(**cleaned)
            config.update(component_generator.config)

        except TypeError as err:
            logger.warning('Problem generating %s: %s', comp_name, str(err))

    config = processors.build_init_files_for_config(config)
    write_config(config)


if __name__ == '__main__':
    main()
