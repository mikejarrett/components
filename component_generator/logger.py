# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger('component_generator')


def set_log_level_to_debug(format_=None):
    if format_ is None:
        format_ = '%(message)s'

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format_)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
