# -*- coding: utf-8 -*-
ABSTRACT_FROM_IMPORTS = 'from component_loader import AbstractComponent\n'
ABSTRACT_INHERITENCE = '(AbstractComponent)'

OBJECT_INHERITENCE = 'object'

ENCODING = '# -*- coding: utf-8 -*-\n'

TEST_CASE_FROM_IMPORTS = 'from unittest import TestCase\n'

EIGHT_SPACES = ' ' * 8
FOUR_SPACES = ' ' * 4
TWELVE_SPACES = ' ' * 12

STORAGE_PREFIX_MAPPING = {
    'storage': set([
        'persist_{0}',
        'retrieve_{0}',
        'update_{0}',
        'delete_{0}',
    ]),
}

LOGIC_PREFIX_MAPPING = {
    'logic': set([
        'create_{0}',
        'get_{0}',
        'update_{0}',
        'delete_{0}',
    ]),
    'client': set([
        'create_{0}',
        'get_{0}',
        'update_{0}',
        'delete_{0}',
    ]),
}
