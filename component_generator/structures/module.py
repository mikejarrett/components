# -*- coding: utf-8 -*-
from component_generator.templates import ALL_TEMPLATE, INIT_FILE_TEMPLATE


class Module(object):  # A file -- foo.py

    def __init__(self, filename, test=False):
        self._filename = filename
        self._classes = set()
        self._all_declarations = set()

        self.test = test
        self._built = False
        self.body = ''

    @property
    def filename(self):
        if self.test:
            filename = 'test_{0}'.format(self._filename)
        else:
            filename = self._filename

        return filename

    @property
    def path(self):
        return '{0}.py'.format(self.filename)

    def build(self):
        if self._classes:
            self.body = '\n\n'.join([klass.build() for klass in self._classes])
            self.body = '{0}\n'.format(self.body.rstrip('\n'))

        elif self._all_declarations:
            components = []
            for component in self._all_declarations:
                components.append("    '{0}',".format(component))

            self.body = ALL_TEMPLATE.format(
                encoding='# -*- coding: utf-8 -*-\n',
                components='\n'.join(components)
            )

        else:
            self.body = INIT_FILE_TEMPLATE.format(
                encoding='# -*- coding: utf-8 -*-',
                from_imports='',
                imports=''
            )

        if self.body:
            self._built = True

        return self.body

    def add_class(self, klass):
        self._classes.add(klass)

    def add_all_declaration(self, klass):
        self._all_declarations.add(klass.underscored_lower)

    def __repr__(self):
        return '<Module {0} (test: {1})>'.format(self.filename, self.test)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((
            self.filename,
            tuple(self._classes),
            tuple(self._all_declarations)
        ))


