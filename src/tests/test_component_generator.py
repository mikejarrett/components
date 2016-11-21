# -*- coding: utf-8 -*-
from unittest import TestCase

from component_generator import ComponentGenerator


class Test(TestCase):

    maxDiff = None

    def test_generate_method_stub_no_args_no_kwargs(self):
        actual = ComponentGenerator.generate_method_stub('persist_evil_dead')
        actual = actual.replace('    ', '')

        expected = 'def persist_evil_dead(self):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_stub_args_no_kwargs(self):
        actual = ComponentGenerator.generate_method_stub(
            'persist_evil_dead',
            ['arg1', 'arg2'],
        )
        actual = actual.replace('    ', '')

        expected = 'def persist_evil_dead(self, arg1, arg2):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_stub_args_and_kwargs(self):
        actual = ComponentGenerator.generate_method_stub(
            'persist_evil_dead',
            ['arg1'],
            [('arg3', 'None')],
        )
        actual = actual.replace('    ', '')

        expected = 'def persist_evil_dead(self, arg1, arg3=None):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_stub_duplicate_args(self):
        actual = ComponentGenerator.generate_method_stub(
            'persist_evil_dead',
            ['arg1', 'arg1'],
        )
        actual = actual.replace('    ', '')

        expected = 'def persist_evil_dead(self, arg1):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_stub_duplicate_args_and_kwargs(self):
        actual = ComponentGenerator.generate_method_stub(
            'persist_evil_dead',
            ['arg1'],
            [('arg1', 'None'), ('arg2', "'Groovy'")]
        )
        actual = actual.replace('    ', '')

        expected = "def persist_evil_dead(self, arg1, arg2='Groovy'):\npass\n"
        self.assertEqual(actual, expected)

    def test_generate_class_old_class_style__python2(self):
        actual = ComponentGenerator.generate_class('Ash', python2=True)
        actual = actual.replace('    ', '')

        expected = 'class Ash(object):\n\n'
        self.assertEqual(actual, expected)

    def test_generate_class_new_class_style(self):
        actual = ComponentGenerator.generate_class('Ash', python2=False)
        actual = actual.replace('    ', '')

        expected = 'class Ash:\n\n'
        self.assertEqual(actual, expected)

    def test_build_file_body(self):
        data = {
            'class_name': 'Component',
            'class_inheritance': ['TestCase'],
            'class_level_arguments': [
                '{0}storage = ComponentPureMemory()'.format(' ' * 4),
                '{0}_internal = None'.format(' ' * 4),
            ],
            'from_imports': [
                ['unittest', 'TestCase'],
                ['component.storage', 'ComponentPureMemory'],
            ],
            'imports': ['os', 'math'],
            'methods': [{
                'name': 'test_create_component',
            }, {
                'name': 'test_get_component_by_id',
            }, {
                'name': 'setUp',
                'additional': [
                    '{0}self.storage = ComponentPureMemory()'.format(' ' * 8),
                ]
            }, {
                'name': 'tearDown',
                'additional': [
                    '{0}self.storage.wipe()'.format(' ' * 8),
                ]
            }]
        }

        actual = ComponentGenerator.build_file_body(data)
        expected = ''.join([
            '# -*- coding: utf-8 -*-\n',
            'from component.storage import ComponentPureMemory\n',
            'from unittest import TestCase\n',
            'import math\n',
            'import os\n',
            '\n\n',
            'class Component(TestCase):\n\n',
            '    storage = ComponentPureMemory()\n',
            '    _internal = None\n\n',
            '    def test_create_component(self):\n',
            '        pass\n\n',
            '    def test_get_component_by_id(self):\n',
            '        pass\n\n',
            '    def setUp(self):\n',
            '        self.storage = ComponentPureMemory()\n\n',
            '    def tearDown(self):\n'
            '        self.storage.wipe()\n\n'
        ])
        self.assertEqual(actual, expected)
