# -*- coding: utf-8 -*-
class Package(object):

    def __init__(self, package_name):
        self.package_name = package_name
        self._modules = []

    def add_module(self, module):
        self._modules.append(module)


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


# ###
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
