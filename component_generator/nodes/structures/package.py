# -*- coding: utf-8 -*-
import errno
import os


def mkdir_p(path):
    """ Mimic *nix 'mkdir -p'. """
    try:
        os.makedirs(path)

    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass

        else:
            raise


def safe_open_w(path):
    """
    Open "path" for writing, creating any parent directories as needed.
    """
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')


class Package(object):  # A directory with an __init__.py file.

    def __init__(self, package_name, test=False):
        self.package_name = package_name
        self._files = set()
        self._sub_packages = set()

        self.path = self.package_name

        self.test = test
        self._built = False

    def add_file(self, files):
        self._files.add(files)

    def add_subpackage(self, package):
        self._sub_packages.add(package)

    def build(self, base_path=''):
        base_path = os.path.join(base_path, self.path)
        self._build_modules(self._files, base_path)

        for sub_package in self._sub_packages:
            sub_base_path = os.path.join(base_path, sub_package.path)
            sub_package.build(base_path)
            self._build_modules(sub_package._files, sub_base_path)

    def _build_modules(self, modules, base_path):
        expected_init_path = os.path.join(base_path, '__init__.py')
        file_paths = []

        for module in modules:
            body = module.build()
            module_path = os.path.join(base_path, module.path)
            with safe_open_w(module_path) as f_:
                f_.write(body)

            file_paths.append(module_path)

        if expected_init_path not in file_paths:
            with safe_open_w(expected_init_path) as f_:
                f_.write('# -*- coding: utf-8 -*-\n')

    def print_file_structure(self, indent_count=0):
        print(' ' * indent_count, '{0}{1}'.format(self.package_name, '/'))
        indent_count += 4
        for file_ in self._files:
            print(' ' * indent_count, file_.path)

            # for klass in file_._classes:
            #     print(klass.body)
            #     print(' ' * (indent_count + 4), 'class {0}'.format(
            #         klass.base_name
            #     ))

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
