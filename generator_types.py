# -*- coding: utf-8 -*-
from collections import namedtuple
import os

import constants
import templates

Thing = namedtuple('Thing', ['prefix_mapping', 'arguments', 'kwarguments'])

class StorageGenerator:

    STORAGE_PREFIX_MAPPING = {
        'storage': set([
            'persist_{0}',
            'retrieve_{0}',
            'update_{0}',
            'delete_{0}',
        ]),
    }

    LOGIC_PREFIX_MAPPING ={
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

    def __init__(
        self,
        name_titled,
        name_underscored_lowered,
        use_abstract_component=True,
        storage_arguments=None,
        storage_kwarguments=None,
        logic_arguments=None,
        logic_kwarguments=None,
        logic_prefix_mapping=None,
        storage_prefix_mapping=None,
        storage_types=None,
        build_on_init=False,
    ):
        """ Instantiate a Storage Generator.
        """
        self.name_titled = name_titled
        self.name_underscored_lowered = name_underscored_lowered
        self.use_abstract_component = use_abstract_component

        if storage_types is None:
            storage_types = ['pure_memory']

        if not isinstance(storage_types, (list, dict)):
            print(
                '`storage_types` is not a list or dict. '
                'Setting to `[pure_memroy]`'
            )
            storage_types = ['pure_memory']

        self.storage_types = storage_types

        self.logic_prefix_mapping = self.LOGIC_PREFIX_MAPPING
        if logic_prefix_mapping is not None:
            self.logic_prefix_mapping = logic_prefix_mapping

        self.storage_prefix_mapping = self.STORAGE_PREFIX_MAPPING
        if storage_prefix_mapping is not None:
            self.storage_prefix_mapping = storage_prefix_mapping

        if storage_arguments and isinstance(storage_arguments, dict):
            self.storage_arguments = storage_arguments
        else:
            self.storage_arguments = {}

        if storage_kwarguments and isinstance(storage_kwarguments, dict):
            self.storage_kwarguments = storage_kwarguments
        else:
            self.storage_kwarguments = {}

        if logic_arguments and isinstance(logic_arguments, dict):
            self.logic_arguments = logic_arguments
        else:
            self.logic_arguments = {}

        if logic_kwarguments and isinstance(logic_kwarguments, dict):
            self.logic_kwarguments = logic_kwarguments
        else:
            self.logic_kwarguments = {}

        self._config = {}

        if build_on_init:
            self.build_configuration()

    def build_configuration(self):
        base_component_path = os.path.join(self.name_underscored_lowered)

        things = (
            Thing(self.logic_prefix_mapping, self.logic_arguments, self.logic_kwarguments),
            Thing(self.storage_prefix_mapping, self.storage_arguments, self.storage_kwarguments),
        )

        for thing in things:
            for component, method_prefixes in thing.prefix_mapping.items():
                sub_component_path = os.path.join(
                    base_component_path,
                    component,
                    '{0}.py'.format(self.name_underscored_lowered)
                )

                if thing.arguments:
                    method_prefixes.add(*list(thing.arguments.keys()))

                if thing.kwarguments:
                    method_prefixes.add(*list(thing.kwarguments.keys()))

                generated_class = self.generate_class(
                    suffix=component.title(),
                    method_prefixes=method_prefixes,
                    method_arguments=thing.arguments,
                    method_kwarguments=thing.kwarguments,
                    is_storage=False,
                )#.rstrip('\n\n')

                self._config[sub_component_path] = generated_class

                # Build __init__.py with __all__ for abstract inheritence.
                if self.use_abstract_component:
                    init_path = os.path.join(
                        base_component_path,
                        component,
                        '__init__.py',
                    )
                    self._config[init_path] = templates.ALL_TEMPLATE.format(
                        encoding=constants.ENCODING,
                        components='{0},'.format(self.name_underscored_lowered),
                    )

                # Build test class(es).
                component_tests_path = os.path.join(
                    base_component_path,
                    'tests',
                    component,
                    'test_{0}.py'.format(self.name_underscored_lowered)
                )
                generated_class = self.generate_class(
                    suffix=component.title(),
                    method_prefixes=method_prefixes,
                    method_arguments={},
                    method_kwarguments={},
                    is_test=True,
                )
                self._config[component_tests_path] = generated_class

    def generate_class(
        self,
        suffix,
        method_prefixes,
        method_arguments,
        method_kwarguments,
        is_test=False,
        is_storage=False,
    ):
        template = templates.METHOD_TEMPLATE
        if is_test:
            template = templates.TEST_METHOD_TEMPLATE

        name_titled = '{prefix}{suffix}'.format(
            prefix=self.name_titled,
            suffix=suffix
        )

        if self.use_abstract_component:
            inheritence = constants.ABSTRACT_INHERITENCE
            from_imports = constants.ABSTRACT_FROM_IMPORTS
        else:
            inheritence=constants.OBJECT_INHERITENCE
            from_imports = ''

        if is_test:
            inheritence = '({0}Interface, TestCase)'.format(self.name_titled)

            if not is_storage:
                inheritence = '(TestCase)'

            name_titled = 'Test{0}{1}'.format(self.name_titled, suffix)
            from_imports = constants.TEST_CASE_FROM_IMPORTS
            method_arguments = {}
            method_kwarguments = {}

        methods = self.build_methods_template(
            underscored_lower=self.name_underscored_lowered,
            template=template,
            method_prefixes=method_prefixes,
            method_arguments=method_arguments,
            method_kwarguments=method_kwarguments,
        )

        formatted = templates.FILE_TEMPLATE.format(
            encoding=constants.ENCODING,
            from_imports=from_imports,
            imports='',
            class_name=name_titled,
            inheritence=inheritence,
            class_level_attributes='',
            methods=''.join(methods),
        ).rstrip('\n')

        return '{0}\n'.format(formatted)

    def build_methods_template(
        self,
        underscored_lower,
        template,
        method_prefixes,
        method_arguments,
        method_kwarguments,
    ):
        methods = []
        for prefix in method_prefixes:
            arguments = method_arguments.get(prefix, [])
            kwarguments = method_kwarguments.get(prefix, {})

            method_name = prefix.format(underscored_lower)

            arguments_docstring = self._format_docstring(
                arguments=arguments,
                kwarguments=kwarguments,
            )
            arg_string = ''
            if arguments:
                arg_string = ', {0}'.format(', '.join(arguments))

            method = template.format(
                method_name=method_name,
                arguments=arg_string,
                kwarguments=self._format_kwargument_parameters(kwarguments),
                docstring=arguments_docstring,
            )
            methods.append(method)

        return methods if methods else ['    pass']

    def _format_kwargument_parameters(self, kwarguments):
        params = []
        for param, default in kwarguments.items():
            params.append('{0}={1}'.format(param, default))

            return ', {0}'.format(', '.join(params))

        return ''

    def _format_docstring(self, arguments, kwarguments):
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
                templates.METHOD_DOCSTRING.format(arguments_docstring=params),
                constants.EIGHT_SPACES,
            )

        return ''
