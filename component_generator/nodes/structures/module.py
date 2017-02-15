# -*- coding: utf-8 -*-
class Module(object):  # A file -- foo.py

    def __init__(self, filename, test=False):
        self.filename = filename
        self._classes = set()
        self._all = set()

        self.test = test
        self._built = False

    def build(self):
        for klass in self._classes:
            klass.build()

        self._built = True

    def add_class(self, klass):
        self._classes.add(klass)

    def add_all(self, klass):
        self._all.add(klass.base_name)

    def __repr__(self):
        return '<Module {0} (test: {1})>'.format(self.filename, self.test)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((
            self.filename,
            tuple(self._classes),
            tuple(self._all)
        ))


