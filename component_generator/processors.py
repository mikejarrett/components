# -*- coding: utf-8 -*-
import json
import logging
import os
from collections import defaultdict
from copy import deepcopy

from component_generator import utils, templates, constants
from component_generator.utils import clean_raw_name


logger = logging.getLogger(__name__)


def clean(component_name, args):
    """
    Build a keyword argments dict to be used when instantiating the Component
    Generator.

    Args:
        component_name (str): The
        args (`obj`: Namespace):

    Returns:
        dict:
    """
    extended_storage_prefix_mapping = extend_storage_prefix_mapping(
        args.storage_types
    )

    logic_arguments = build_arguments(
        args.logic_arguments,
        component_name
    )
    logic_kwarguments = build_kwarguments(
        args.logic_kwarguments,
        component_name
    )

    storage_arguments = build_arguments(
        args.storage_arguments,
        component_name
    )
    storage_kwarguments = build_kwarguments(
        args.storage_kwarguments,
        component_name
    )

    names = clean_raw_name(component_name)

    return {
        'storage_prefix_mapping': extended_storage_prefix_mapping,
        'logic_arguments': logic_arguments,
        'logic_kwarguments': logic_kwarguments,
        'storage_arguments': storage_arguments,
        'storage_kwarguments': storage_kwarguments,
        'name_titled': names.titled,
        'name_underscored_lowered': names.underscored_lower,
        'path': args.path,
    }


def extend_storage_prefix_mapping(storage_types):
    """ Extend the default storage prefix mapping with additonal storage types.

    Args:
        storage_types (list): A list of strings of additional storage types
            to be generated.

    Returns:
        dict: Of extended prefix mappings.
    """
    storage_prefix_mapping = {}
    prefixes = constants.STORAGE_PREFIX_MAPPING['storage']
    for storage in storage_types + ['pure_memory']:
        path = os.path.join(
            'storage',
            utils.clean_raw_name(storage).underscored_lower,
        )
        storage_prefix_mapping[path] = prefixes

    return storage_prefix_mapping


def build_arguments(arguments, component_name):
    try:
        methods = json.loads(arguments)
    except ValueError as err:
        logger.warning(
            'Got "%s" when attempting to decode -- %s --. Ignoring '
            '`arguments` and setting to {}',
            str(err),
            methods
        )
        methods = {}

    method_definitions = methods.get(component_name, {})
    method_definitions_copy = deepcopy(method_definitions)
    for method, args in method_definitions_copy.items():
        if not isinstance(args, (list, set)):
            method_definitions[method] = [args]

    return method_definitions


def build_kwarguments(kwarguments, component_name):
    try:
        methods = json.loads(kwarguments)
    except ValueError as err:
        logger.warning(
            'Got "%s" when attempting to decode -- %s --. Ignoring '
            '`kwarguments` and setting to {}',
            str(err),
            kwarguments
        )
        return {}

    method_definitions = methods.get(component_name, {})
    if not isinstance(method_definitions, dict):
        logger.warning('Logic kwarguments not in correct format.')
        return {}

    method_definitions_copy = deepcopy(method_definitions)
    for method, args in method_definitions_copy.items():
        if not isinstance(args, dict):
            logger.warning(
                'Removing `%s` from kwarguments because its key-value '
                'pairs not presented as a dictionary. (%s)',
                method,
                args,
            )
            del method_definitions[method]

    return method_definitions


def build_init_files_for_config(config, use_abstract_component=True):
    """ Make sure every package has an __init__.py file.

    Args:
        config (dict): A dictionary that was generated from the component
            generator.
        use_abstract_component (`obj`: bool, optional): If we are inheriting
            from AbstractComponent, define __all__ with the appropraite
            modules.
    Returns:
        dict: Update config dict with __init__.py defined.
    """
    empty_init_file = templates.INIT_FILE_TEMPLATE.format(
        encoding=constants.ENCODING,
        from_imports='',
        imports=''
    )

    files_and_paths = defaultdict(list)
    for filepath in config:
        base_path, filename = os.path.split(filepath)
        files_and_paths[base_path].append(filename)

        filepath_list = os.path.split(filepath)[0].split(os.sep)
        if 'component' in filepath_list:
            component_index = filepath_list.index('component')

            path = os.path.join(os.sep, *filepath_list[:component_index])

            for index, __ in enumerate(filepath_list[component_index:]):
                index += 1
                path_list = filepath_list[component_index:component_index + index]
                package_path = os.path.join(path, *path_list)

                files_and_paths[package_path].append('')

    for base_path, filenames in files_and_paths.items():
        init_file_path = os.path.join(base_path, '__init__.py')

        if '__init__.py' not in filenames:
            logger.debug('Generating: %s', init_file_path)
            config[init_file_path] = empty_init_file

        elif '__init__.py' in filenames and use_abstract_component:
            logger.debug('Generating __all__: %s', init_file_path)

            files = []
            for file_ in filenames:
                if file_ in ['__init__.py', '']:
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
