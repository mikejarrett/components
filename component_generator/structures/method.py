# -*- coding: utf-8 -*-
from component_generator import constants
from component_generator.templates import (
    METHOD_DOCSTRING,
    METHOD_TEMPLATE,
    TEST_METHOD_TEMPLATE
)


class Method(object):  # A method -- def persist_{0}(self):

    def __init__(self, name, object_name, test=False):
        self.name = name
        self.object_name = object_name
        self._arguments = []
        self._kwarguments = {}

        self.test = test
        self._built = False
        self.body = ''

    def add_argument(self, argument):
        self._arguments.append(argument)

    def add_kwargument(self, key, value):
        if key in self._arguments:
            self._arguments.pop(key)

        self._kwarguments[key] = value

    def build(self):
        template = METHOD_TEMPLATE
        if self.test:
            template = TEST_METHOD_TEMPLATE

        arguments_docstring = self._format_docstring(
            arguments=self._arguments,
            kwarguments=self._kwarguments,
        )

        arg_string = ''
        if self._arguments:
            arg_string = ', {0}'.format(', '.join(self._arguments))

        self.body = template.format(
            method_name=self.name.format(self.object_name),
            arguments=arg_string,
            kwarguments=self._format_kwargument_parameters(),
            docstring=arguments_docstring,
        )

        self._built = True
        return self.body

    def __repr__(self):
        return '<Method {0} (test: {1})>'.format(self.name, self.test)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((
            self.name,
            self.object_name,
            tuple(self._arguments),
            tuple(self._kwarguments.keys()),
        ))

    def _format_kwargument_parameters(self):
        params = []
        for param, default_value in self._kwarguments.items():
            params.append('{0}={1}'.format(param, default_value))

            return ', {0}'.format(', '.join(params))

        return ''

    @staticmethod
    def _format_docstring(arguments, kwarguments):
        parameters = arguments + list(kwarguments.keys())
        if parameters:
            params = ''
            for param in parameters:
                params += '{0}{1} (TODO):\n'.format(
                    constants.TWELVE_SPACES,
                    param
                )

            params.rstrip('\n')

            return '{0}{1}'.format(
                METHOD_DOCSTRING.format(arguments_docstring=params),
                constants.EIGHT_SPACES,
            )

        return ''
