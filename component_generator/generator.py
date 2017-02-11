# -*- coding: utf-8 -*-
import logging
import os
from collections import namedtuple, defaultdict

from component_generator import constants, templates, utils


logger = logging.getLogger(__name__)


Subcomponent = namedtuple(
    'Subcomponent',
    ['prefix_mapping', 'arguments', 'kwarguments']
)


class ComponentGenerator:

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

    def __init__(  # pylint: disable=too-many-branches
        self,
        name_titled,
        name_underscored_lowered,
        use_abstract_component=True,
        logic_arguments=None,
        logic_kwarguments=None,
        logic_prefix_mapping=None,
        storage_arguments=None,
        storage_kwarguments=None,
        storage_prefix_mapping=None,
    ):
        self.name_titled = name_titled
        self.name_underscored_lowered = name_underscored_lowered
        self.use_abstract_component = use_abstract_component

        self._logic_prefix_mapping = self.LOGIC_PREFIX_MAPPING
        if logic_prefix_mapping is not None:
            self._logic_prefix_mapping = logic_prefix_mapping

        self._storage_prefix_mapping = self.STORAGE_PREFIX_MAPPING
        if storage_prefix_mapping is not None:
            self._storage_prefix_mapping = storage_prefix_mapping

        if storage_arguments and isinstance(storage_arguments, dict):
            self._storage_arguments = storage_arguments
        else:
            self._storage_arguments = {}

        if storage_kwarguments and isinstance(storage_kwarguments, dict):
            self._storage_kwarguments = storage_kwarguments
        else:
            self._storage_kwarguments = {}

        if logic_arguments and isinstance(logic_arguments, dict):
            self._logic_arguments = logic_arguments
        else:
            self._logic_arguments = {}

        if logic_kwarguments and isinstance(logic_kwarguments, dict):
            self._logic_kwarguments = logic_kwarguments
        else:
            self._logic_kwarguments = {}

        self.config = {}
        self.build_configuration()

    def build_configuration(self):
        base_path = os.path.join('component') #self.name_underscored_lowered)

        subcomponents = (
            Subcomponent(
                self._logic_prefix_mapping,
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
            for part in reversed(component.split(os.path.sep))
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
                suffix=component.title(),
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

    @staticmethod
    def build_init_files_for_config(config, use_abstract_component=True):
        empty_init_file = templates.INIT_FILE_TEMPLATE.format(
            encoding=constants.ENCODING,
            from_imports='',
            imports=''
        )

        files_and_paths = defaultdict(list)
        for filepath in config:
            base_path, filename = os.path.split(filepath)
            files_and_paths[base_path].append(filename)

        for base_path, filenames in files_and_paths.items():
            init_file_path = os.path.join(base_path, '__init__.py')

            if '__init__.py' not in filenames:
                logger.debug('Generating: %s', init_file_path)
                config[init_file_path] = empty_init_file

            elif '__init__.py' in filenames and use_abstract_component:
                logger.debug('Generating __all__: %s', init_file_path)

                files = []
                for file_ in filenames:
                    if file_ == '__init__.py':
                        continue

                    files.append(
                        "{spaces}'{name}',".format(
                            spaces=constants.FOUR_SPACES,
                            name=os.path.splitext(file_)[0]
                        )
                    )

                config[init_file_path] = templates.ALL_TEMPLATE.format(
                    encoding=constants.ENCODING,
                    components='\n'.join(files)
                )

        return config

    @classmethod
    def build_storage_prefix_mapping(cls, storages):
        storage_prefix_mapping = {}
        prefixes = cls.STORAGE_PREFIX_MAPPING['storage']
        for storage in storages + ['pure_memory']:
            path = os.path.join(
                'storage',
                utils.clean_raw_name(storage).underscored_lower,
            )
            storage_prefix_mapping[path] = prefixes

        return storage_prefix_mapping
