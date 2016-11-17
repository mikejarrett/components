# -*- coding: utf-8 -*-
from unittest import TestCase

from component import ComponentGenerator


class Test(TestCase):

    component = ComponentGenerator()

    def test_generate_method_name_no_args_no_kwargs(self):
        actual = self.component.generate_method_name('persist_mouse')
        actual = actual.replace('    ', '')

        expected = 'def persist_mouse(self):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_name_args_no_kwargs(self):
        actual = self.component.generate_method_name(
            'persist_mouse',
            ['arg1', 'arg2'],
        )
        actual = actual.replace('    ', '')

        expected = 'def persist_mouse(self, arg1, arg2):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_name_args_and_kwargs(self):
        actual = self.component.generate_method_name(
            'persist_mouse',
            ['arg1'],
            [('arg3', 'None')],
        )
        actual = actual.replace('    ', '')

        expected = 'def persist_mouse(self, arg1, arg3=None):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_name_duplicate_args(self):
        actual = self.component.generate_method_name(
            'persist_mouse',
            ['arg1', 'arg1'],
        )
        actual = actual.replace('    ', '')

        expected = 'def persist_mouse(self, arg1):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_name_duplicate_args_and_kwargs(self):
        actual = self.component.generate_method_name(
            'persist_mouse',
            ['arg1'],
            [('arg1', 'None'), ('arg2', "'Tasty'")]
        )
        actual = actual.replace('    ', '')

        expected = "def persist_mouse(self, arg1, arg2='Tasty'):\npass\n"
        self.assertEqual(actual, expected)
