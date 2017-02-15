# -*- coding: utf-8 -*-
class Package(object):  # A directory with an __init__.py file.

    def __init__(self, package_name, test=False):
        self.package_name = package_name
        self._files = set()
        self._sub_packages = set()

        self.test = test
        self._built = False

    def add_file(self, files):
        self._files.add(files)

    def add_subpackage(self, package):
        self._sub_packages.add(package)

    def build(self):
        for file_ in self._files:
            file_.build()

        for package in self._sub_packages:
            package.build()

        self._built = True

    def print_file_structure(self, indent_count=0):
        print(' ' * indent_count, '{0}{1}'.format(self.package_name, '/'))
        indent_count += 4
        for file_ in self._files:
            print(' ' * indent_count, '{0}{1}'.format(file_.filename, '.py'))
            for klass in file_._classes:
                print(klass.body)
                # print(' ' * (indent_count + 4), 'class {0}'.format(klass.base_name))
                # for method in klass._methods:
                #     print(method.body)
                #     kwargs = ','.join(
                #         [
                #             "'{}'={}".format(key, value)
                #             for key, value in method._kwarguments.items()
                #         ]
                #     )
                #     args = ','.join(list(method._arguments)) + kwargs
                #     print(' ' * (indent_count + 8), 'def {0}(self, {1})'.format(method.name, args))

        for package in self._sub_packages:
            package.print_file_structure(indent_count)

    def __repr__(self):
        return '<Package {0} (test: {1})>'.format(self.package_name, self.test)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((
            self.package_name,
            tuple(self._files),
            tuple(self._sub_packages),
            self.test
        ))
