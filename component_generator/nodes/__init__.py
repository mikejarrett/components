# -*- coding: utf-8 -*-
class Combiner(object):

    def __init__(self, **kwargs):
        self._names_titled = kwargs.get('names_titled', [])
        self._names_underscored_lowered = kwargs.get('names_underscored_lowered', [])
        self._logic_prefix_mapping = kwargs.get('logic_prefix_mapping', {})
        self._storage_prefix_mapping = kwargs.get('storage_prefix_mapping', {})
        self._path = kwargs.get('path', '')

    def build(self):
        root_package = Package('blah')
        for package, methods in self._logic_prefix_mapping.items():
            # Package(logic)
            # Package(client)
            package = Package(package)

            for name in self._names_underscored_lowered:
                # Klass(Foo)
                klass = Klass(name)

                for method in methods:
                    # Method(create_{0})
                    # Method(update_{0})
                    # ...
                    klass.add_method(Method(method))

                # Module(foo.py)
                module = Module(name)
                package.add_module(module)

        for package, methods in self._storage_prefix_mapping.items():
            # Package(storage)
            package = Package(package)

            for name in self._names_underscored_lowered:
                # Klass(Foo)
                klass = Klass(name)

                for method in methods:
                    # Method(persist_{0})
                    # Method(update_{0})
                    # ...
                    klass.add_method(Method(method))

                # Module(foo.py)
                module = Module(name)
                package.add_module(module)

            root_package.add_subpackage(package)


class Package(object):

    def __init__(self, package_name):
        self.package_name = package_name
        self._modules = []
        self._sub_packages = []

    def add_module(self, module):
        self._modules.append(module)

    def add_subpackage(self, package):
        self._sub_packages.append(package)

    def build(self):
        pass


class Module(object):

    def __init__(self, filename):
        self.filename = filename
        self._classes = []
        self._all = []

    def add_class(self, klass):
        self._classes.append(klass)

    def add_all(self, klass):
        self._all.append(klass.base_name)


class Klass(object):

    def __init__(self, base_name):
        self.base_name = base_name
        self._methods = []

    def add_method(self, method):
        self._methods.append(method)


class Method(object):

    def __init__(self, name):
        self.name = name
        self._arguments = []
        self._kwarguments = {}

    def add_argument(self, argument):
        self._arguments.append(argument)

    def add_kwargument(self, key, value):
        if key in self._arguments:
            self._arguments.pop(key)

        self._kwarguments[key] = value


######
# component_loader bar foo


# # Build bar
# persist_method = Method(persist_{0})

# klass = Klass(Bar)
# klass.add_method(persist_method)

# bar_module = Module(bar)  # bar.py
# bar_module.add_class(klass)

# bar_package = Package(pure_memory)
# bar_package.add_module(bar_module)

# # Build foo
# persist_method = Method(persist_{0})

# klass = Klass(foo)
# klass.add_method(persist_method)

# foo_module = Module(foo)  # foo.py
# foo_module.add_class(klass)

# foo_package = Package(pure_memory)
# foo_package.add_module(foo_module)

# storage_package = Package(storage)
# storage_package.add_subpackage(bar_package)
# storage_package.add_subpackage(foo_package)

# component_package = Package(component)
# component_package.add_subpackage(storage_package)
