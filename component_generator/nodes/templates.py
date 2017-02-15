# -*- coding: utf-8 -*-
INIT_FILE_TEMPLATE = """{encoding}{from_imports}{imports}"""

FILE_TEMPLATE = """\
{encoding}{from_imports}{imports}

class {class_name}{inheritence}:
{class_level_attributes}
{methods}
"""

METHOD_DOCSTRING = '''\
"""
        Args:
{arguments_docstring}
        """
'''

METHOD_TEMPLATE = """\
    def {method_name}(self{arguments}{kwarguments}):
        {docstring}raise NotImplementedError('Please implement: {method_name}')

"""

TEST_METHOD_TEMPLATE = """\
    def test_{method_name}(self):
        raise NotImplementedError('Please implement: test_{method_name}')

"""

ALL_TEMPLATE = """{encoding}__all__ = [\n{components}\n]\n"""
