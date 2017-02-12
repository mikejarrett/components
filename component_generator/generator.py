# -*- coding: utf-8 -*-
from copy import deepcopy
import json
import logging
import os
from collections import namedtuple, defaultdict

from component_generator import constants, templates, utils

try:
    from os import getcwdu as getcwd
except ImportError:  # Hurray we're using Python 3!
    from os import getcwd


logger = logging.getLogger(__name__)


Subcomponent = namedtuple(
    'Subcomponent',
    ['prefix_mapping', 'arguments', 'kwarguments']
)


class ComponentGenerator:

    def __init__(
        self,
        name_titled,
        name_underscored_lowered,
        storage_prefix_mapping,
        logic_arguments,
        logic_kwarguments,
        storage_arguments,
        storage_kwarguments,
        use_abstract_component=True,
        path=None,
    ):
        self.name_titled = name_titled
        self.name_underscored_lowered = name_underscored_lowered
        self.use_abstract_component = use_abstract_component

        self._storage_prefix_mapping = storage_prefix_mapping
        self._storage_arguments = storage_arguments
        self._storage_kwarguments = storage_kwarguments

        self._logic_arguments = logic_arguments
        self._logic_kwarguments = logic_kwarguments

        self.path = path
        if path is None:
            self.path = getcwd()

        self.config = {}
        self.build_configuration()

    def build_configuration(self):
        base_path = os.path.join(os.path.normpath(self.path), 'component')

        subcomponents = (
            Subcomponent(
                constants.LOGIC_PREFIX_MAPPING,
                self._logic_arguments,
                self._logic_kwarguments,
            ),
            Subcomponent(
                self._storage_prefix_mapping,
                self._storage_arguments,
                self._storage_kwarguments,
            ),
        )

        for subcomponent in subcomponents:
            self._process_subcomponent(base_path, subcomponent)

    def _get_suffix(self, component):
        return ''.join(
            utils.clean_raw_name(part).titled_no_underscore
            for part in reversed(component.split(os.sep))
        )

    def _process_subcomponent(self, base_path, subcomponent):
        for component, method_prefixes in subcomponent.prefix_mapping.items():

            sub_component_path = os.path.join(
                base_path,
                component,
                '{0}.py'.format(self.name_underscored_lowered)
            )

            if subcomponent.arguments:
                method_prefixes.add(*list(subcomponent.arguments.keys()))

            if subcomponent.kwarguments:
                method_prefixes.add(*list(subcomponent.kwarguments.keys()))

            suffix = self._get_suffix(component)
            generated_class = self.generate_class(
                suffix=suffix,
                method_prefixes=method_prefixes,
                method_arguments=subcomponent.arguments,
                method_kwarguments=subcomponent.kwarguments,
                is_storage=False,
            )

            self.config[sub_component_path] = generated_class

            # Build __init__.py with __all__ for abstract inheritence.
            if self.use_abstract_component:
                init_path = os.path.join(
                    base_path,
                    component,
                    '__init__.py',
                )
                self.config[init_path] = templates.ALL_TEMPLATE.format(
                    encoding=constants.ENCODING,
                    components="", #'{0}',".format(self.name_underscored_lowered),
                )

            # Build test class(es).
            component_tests_path = os.path.join(
                base_path,
                'tests',
                component,
                'test_{0}.py'.format(self.name_underscored_lowered)
            )
            generated_class = self.generate_class(
                suffix=suffix,
                method_prefixes=method_prefixes,
                method_arguments={},
                method_kwarguments={},
                is_test=True,
            )
            self.config[component_tests_path] = generated_class

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
        name_titled = '{prefix}{suffix}'.format(
            prefix=self.name_titled,
            suffix=suffix
        )

        if self.use_abstract_component:
            inheritence = constants.ABSTRACT_INHERITENCE
            from_imports = constants.ABSTRACT_FROM_IMPORTS
        else:
            inheritence = constants.OBJECT_INHERITENCE
            from_imports = ''

        if is_test:
            template = templates.TEST_METHOD_TEMPLATE
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
            class_level_attributes='',  # TODO - also include leading spaces
            methods=''.join(methods),
        ).rstrip('\n')

        # Add a new line to the end of the file.
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

    @staticmethod
    def _format_kwargument_parameters(kwarguments):
        params = []
        for param, default in kwarguments.items():
            params.append('{0}={1}'.format(param, default))

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
                templates.METHOD_DOCSTRING.format(arguments_docstring=params),
                constants.EIGHT_SPACES,
            )

        return ''
