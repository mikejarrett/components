# -*- coding: utf-8 -*-
from component_generator.structures import Klass, Method, Module, Package
from component_generator import constants


class Generator(object):

    def __init__(self, **kwargs):
        self._names = kwargs.get('names', [])
        self._api_methods = constants.LOGIC_METHODS
        self._storage_methods = constants.STORAGE_METHODS
        self._path = kwargs.get('path', '')
        self._storage_types = kwargs.get('storage_types', ['pure_memory'])
        self._additional_methods = kwargs.get('additional', {})

        self.root_package_name = kwargs.get('root_package_name', 'component')

        self.blank_init_module = Module('__init__')

    def build(self):
        root_test_package = Package('tests')
        root_test_package.add_file(self.blank_init_module)

        root_package = Package(self.root_package_name)
        root_package.add_subpackage(root_test_package)
        root_package.add_file(self.blank_init_module)

        root_package, root_test_package = self._build_api_package(
            root_package=root_package,
            root_test_package=root_test_package,
        )

        root_package, __ = self._build_storage_package(
            root_package=root_package,
            root_test_package=root_test_package,
        )

        root_package.build()

        return root_package

    def _build_api_package(self, root_package, root_test_package):
        for package, methods in self._api_methods.items():
            api_package = Package(package)
            api_test_package = Package(package)
            init_module = Module('__init__')

            for name in self._names:
                klass = Klass(name, package)
                test_klass = Klass(name, package, test=True)

                module = Module(name.name_underscored_lowered)
                test_module = Module(name.name_underscored_lowered, test=True)

                for method in methods:
                    method_ = Method(
                        method,
                        name.name_underscored_lowered,
                    )
                    klass.add_method(method_)

                    test_method_ = Method(
                        method,
                        name.name_underscored_lowered,
                        test=True,
                    )
                    test_klass.add_method(test_method_)

                additional_methods = self._additional_methods.get(name.raw, {})
                for method, args_kwargs in additional_methods.items():
                    method_ = self._build_method_args_kwargs(
                        Method(
                            method,
                            name.name_underscored_lowered,
                        ),
                        args_kwargs
                    )

                    klass.add_method(method_)

                    test_method_ = Method(
                        method,
                        name.name_underscored_lowered,
                        test=True,
                    )
                    test_klass.add_method(test_method_)

                module.add_class(klass)
                api_package.add_file(module)

                test_module.add_class(test_klass)
                api_test_package.add_file(test_module)

                init_module.add_all_declaration(klass)

            api_package.add_file(init_module)

            # Add built api_package to root_package.
            root_package.add_subpackage(api_package)

            root_test_package.add_subpackage(api_test_package)

        return root_package, root_test_package

    def _build_storage_package(self, root_package, root_test_package):
        for package, methods in self._storage_methods.items():
            storage_package = Package(package)
            storage_package.add_file(self.blank_init_module)

            test_package = Package(package)

            for storage_type in self._storage_types:
                package = Package(storage_type)

                for name in self._names:
                    klass = Klass(name, storage_type)
                    test_klass = Klass(name, storage_type, test=True)

                    module = Module(name.name_underscored_lowered)
                    test_module = Module(
                        name.name_underscored_lowered,
                        test=True
                    )

                    for method in methods:
                        method_ = Method(method, name.name_underscored_lowered)
                        klass.add_method(method_)

                        test_method_ = Method(
                            method,
                            name.name_underscored_lowered,
                            test=True
                        )
                        test_klass.add_method(test_method_)

                    for method in self._additional_methods.get(name.raw, {}):
                        method_ = self._build_method_args_kwargs(
                            Method(method, name.name_underscored_lowered),
                            []
                        )

                        klass.add_method(method_)

                        test_method_ = Method(
                            method,
                            name.name_underscored_lowered,
                            test=True
                        )
                        test_klass.add_method(test_method_)

                    module.add_class(klass)
                    package.add_file(module)

                    test_module.add_class(test_klass)
                    test_package.add_file(test_module)

                # Add built package to storage_package
                storage_package.add_subpackage(package)

            # Add built storage_package to root_package
            root_package.add_subpackage(storage_package)

            root_test_package.add_subpackage(test_package)

        return root_package, root_test_package

    def _build_method_args_kwargs(self, method, args_kwargs):
        for item in args_kwargs:
            if isinstance(item, list):
                for arg in item:
                    method.add_argument(arg)

            elif isinstance(item, dict):
                for keyword, argument in item.items():
                    method.add_kwargument(keyword, argument)

        return method
