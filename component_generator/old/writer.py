# -*- coding: utf-8 -*-
import errno
import logging
import os

logger = logging.getLogger(__name__)

def mkdir_p(path):
    """ Mimic *nix 'mkdir -p'. """
    try:
        os.makedirs(path)

    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass

        else:
            raise


def safe_open_w(path):
    """
    Open "path" for writing, creating any parent directories as needed.
    """
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')


def write_config(generator_config):
    for path, data in generator_config.items():
        logger.debug('Writing: %s', path)
        try:
            with safe_open_w(path) as file_:
                file_.write(data)
        except OSError:
            logger.exception("Couldn't write: %s", path)
