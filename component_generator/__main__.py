#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=redefined-builtin,invalid-name
import logging

from component_generator.generator import ComponentGenerator
from component_generator.utils import clean_raw_name
from component_generator.writer import write_config


try:
    input = raw_input
except NameError:  # Python 3
    pass


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    component_name = input('Component Name: ')

    names = clean_raw_name(component_name)
    component_generator = ComponentGenerator(
        name_titled=names.titled,
        name_underscored_lowered=names.underscored_lower
    )

    write_config(component_generator.config)
