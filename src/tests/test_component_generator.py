# -*- coding: utf-8 -*-
from unittest import TestCase

from component_generator import ComponentGenerator


class Test(TestCase):

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

        expected = 'class Ash(object):\n'
        self.assertEqual(actual, expected)

    def test_generate_class_new_class_style(self):
        actual = ComponentGenerator.generate_class('Ash', python2=False)
        actual = actual.replace('    ', '')

        expected = 'class Ash:\n'
        self.assertEqual(actual, expected)