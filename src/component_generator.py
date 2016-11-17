# -*- coding: utf-8 -*-
from collections import OrderedDict


CLASS_TEMPLATE = '''class {class_name}{python2_formatting}:\n'''
METHOD_TEMPLATE = '''    def {method_name}(self{arguments}{kwarguments}):\n        pass\n'''


class ComponentGenerator:

    def generate_class(self, class_name, python2=False):
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

    def generate_method_stub(
        self,
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

        formatted_arguments = self._format_method_arguments(arguments)
        formatted_kwarguments = self._format_method_kwarguments(
            kwarguments,
            arguments
        )

        return METHOD_TEMPLATE.format(
            method_name=method_name,
            arguments=formatted_arguments,
            kwarguments=formatted_kwarguments,
        )

    def _format_method_arguments(self, arguments):
        if isinstance(arguments, (list, tuple, set)):
            arguments = ', {}'.format(', '.join(arguments))

        else:
            arguments = ''

        return arguments

    def _format_method_kwarguments(self, kwarguments, arguments):
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
