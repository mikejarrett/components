# -*- coding: utf-8 -*-
from component_generator import constants
from component_generator.templates import FILE_TEMPLATE


class Klass(object):

    def __init__(self, name, type_, test=False):
        self.base_name = name.titled
        self.underscored_lower = name.name_underscored_lowered

        self.type_ = type_.title()
        self._methods = set()

        self.test = test
        self._built = False
        self.body = ''

    def add_method(self, method):
        self._methods.add(method)

    def build(self):
        methods = [method.build() for method in self._methods]
        if not methods:
            methods = ['{0}pass'.format(constants.FOUR_SPACES)]

        from_imports = self._get_from_imports()
        imports = self._get_imports()
        inheritence = self._get_inheritence()
        class_name = self._get_class_name()

        formatted = FILE_TEMPLATE.format(
            encoding='# -*- coding: utf-8 -*-\n',
            from_imports=from_imports,
            imports=imports,
            class_name=class_name,
            inheritence=inheritence,
            class_level_attributes='',  # TODO
            methods=''.join(methods),
        ).rstrip('\n')

        # Add a new line to the end of the file.
        self.body = '{0}\n'.format(formatted)

        self._built = True
        return self.body

    def __repr__(self):
        return '<Klass {0} (test: {1})>'.format(self.base_name, self.test)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((
            self.base_name,
            tuple(self._methods),
        ))

    def _get_from_imports(self):
        # FIXME
        return 'from component_loader import AbstractComponent'

    def _get_imports(self):
        # FIXME
        return ''

    def _get_inheritence(self):
        # FIXME
        if self.test:
            return '(object)'
        else:
            return '(AbstractComponent)'

    def _get_class_name(self):
        class_name = '{0}{1}'.format(self.base_name, self.type_)
        if self.test:
            class_name = 'Test{0}'.format(class_name)

        return class_name
