# -*- coding: utf-8 -*-
from collections import OrderedDict


ENCODING = '# -*- coding: utf-8 -*-'
BLANK_LINE = '\n'
IMPORT_TEMPLATE = 'import {import_name}'
FROM_IMPORT_TEMPLATE = 'from {module_path} import {import_name}'
CLASS_TEMPLATE = 'class {class_name}{python2_formatting}:\n'
METHOD_TEMPLATE = '    def {method_name}(self{arguments}{kwarguments}):\n        pass\n'


class ComponentGenerator:

    @classmethod
    def build_file_body(cls, data):
        """ Take a dictionary structure and build a file's body.

        Structure of data:
            {
                'from_imports': [[0, 1]] ``list`` of ``list``, [0] is import
                    path and [1] is the thing we are importing,
                'imports': ``list`` of import names,
                'class_name': ``str``,
                'python2': ``bool``,
                'methods': [
                    {
                        'name': ``str``,
                        'args': ``list`` of ``str`` representing args
                            (optional),
                        'kwargs': ``list`` of ``list`` of keyword args
                            (optional),
                    },
                ],
            }
        """
        body = [
            ENCODING,
            BLANK_LINE,
        ]

        imports_available = False
        if 'from_imports' in data:
            imports_available = True
            for imports in data['from_imports']:
                body.extend([
                    FROM_IMPORT_TEMPLATE.format(
                        module_path=imports[0],
                        import_name=imports[1]
                    ),
                    BLANK_LINE
                ])

        if 'imports' in data:
            imports_available = True
            pass

        if not imports_available and not data.get('__init__', False):
            body.extend([
                BLANK_LINE,
                BLANK_LINE,
            ])

        if 'class_name' in data:
            python2 = data.get('python2', False)
            class_name = data['class_name']
            body.extend([
                cls.generate_class(class_name, python2),
                BLANK_LINE,
            ])

        if 'methods' in data:
            for method in data['methods']:
                body.extend([
                    cls.generate_method_stub(
                        method['name'],
                        method.get('args', []),
                        method.get('kwargs', [])
                    ),
                    BLANK_LINE,
                ])

        return ''.join(body)

    @staticmethod
    def generate_class(class_name, python2=False):
        """ Geneate a method stub for the given name, args and kwargs.

        Stub a method that will be in the style of standard python formatting:

            class ClassName:

            or

            class ClassName(object):

        Args:
            class_name (str): Name to apply to the class.
            python2 (boolean): If ``True`` add the Python2 style formatting
                when generating the class. (object)


        Returns:
            str: That will represent the class with the desired parameters.
        """

        python2_formatting = ''
        if python2:
            python2_formatting = '(object)'

        return CLASS_TEMPLATE.format(
            class_name=class_name,
            python2_formatting=python2_formatting,
        )

    @classmethod
    def generate_method_stub(
        cls,
        method_name,
        arguments=None,
        kwarguments=None
    ):
        """ Geneate a method stub for the given name, args and kwargs.

        Stub a method that will be in the style of standard python formatting:

            def method_name(self, arg1, arg2=None):
                pass

        Args:
            method_name (str): Name to apply to the method.
            arguments (list): A list of strings the method will take.
            kwarguments (list): A list of ``tuples`` / ``list`` of
                (``str``, ``str``) where the first string is the name of the
                argument and the string is the default value.

        Returns:
            str: That will represent the method with the desired parameters.
        """
        if isinstance(arguments, (list, tuple, set)):
            # Remove duplicate keys (``set`` is unordered.)
            arguments = list(OrderedDict.fromkeys(arguments).keys())

        formatted_arguments = cls._format_method_arguments(arguments)
        formatted_kwarguments = cls._format_method_kwarguments(
            kwarguments,
            arguments
        )

        return METHOD_TEMPLATE.format(
            method_name=method_name,
            arguments=formatted_arguments,
            kwarguments=formatted_kwarguments,
        )

    @staticmethod
    def _format_method_arguments(arguments):
        if isinstance(arguments, (list, tuple, set)):
            arguments = ', {}'.format(', '.join(arguments))

        else:
            arguments = ''

        return arguments

    @staticmethod
    def _format_method_kwarguments(kwarguments, arguments):
        if isinstance(kwarguments, (list, tuple, set)):
            new_kwargs = []

            for kwarg in kwarguments:
                if (
                    isinstance(kwarg, (list, tuple, set)) and
                    len(kwarg) == 2 and
                    kwarg[0] not in arguments
                ):
                    new_kwargs.append(
                        '{name}={value}'.format(name=kwarg[0], value=kwarg[1])
                    )

            if new_kwargs:
                kwarguments = ', {}'.format(', '.join(new_kwargs))

        else:
            kwarguments = ''

        return kwarguments
