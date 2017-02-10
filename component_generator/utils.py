# -*- coding: utf-8 -*-
import logging
import re
from collections import namedtuple


logger = logging.getLogger(__name__)


Names = namedtuple(
    'Names',
    [
        'titled',
        'underscored_lower',
        'underscored_titled',
    ]
)


def clean_string(string):
    # Remove invalid characters.
    cleaned_name = re.sub('[^0-9a-zA-Z_ ]', '', string)

    # Remove leading characters until we find a letter or underscore.
    return re.sub('^[^a-zA-Z_]+', '', cleaned_name)


def clean_raw_name(raw_name):
    cleaned = clean_string(raw_name)
    words = cleaned.split(' ')

    return Names(
        titled=''.join([word.title() for word in words]),
        underscored_lower='_'.join([word.lower() for word in words]),
        underscored_titled='_'.join([word.title() for word in words]),
    )
