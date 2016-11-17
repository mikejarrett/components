# -*- coding: utf-8 -*-
from unittest import TestCase

from component import ComponentGenerator


class Test(TestCase):

    component = ComponentGenerator()

    def test_generate_method_stub_no_args_no_kwargs(self):
        actual = self.component.generate_method_stub('persist_evil_dead')
        actual = actual.replace('    ', '')

        expected = 'def persist_evil_dead(self):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_stub_args_no_kwargs(self):
        actual = self.component.generate_method_stub(
            'persist_evil_dead',
            ['arg1', 'arg2'],
        )
        actual = actual.replace('    ', '')

        expected = 'def persist_evil_dead(self, arg1, arg2):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_stub_args_and_kwargs(self):
        actual = self.component.generate_method_stub(
            'persist_evil_dead',
            ['arg1'],
            [('arg3', 'None')],
        )
        actual = actual.replace('    ', '')

        expected = 'def persist_evil_dead(self, arg1, arg3=None):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_stub_duplicate_args(self):
        actual = self.component.generate_method_stub(
            'persist_evil_dead',
            ['arg1', 'arg1'],
        )
        actual = actual.replace('    ', '')

        expected = 'def persist_evil_dead(self, arg1):\npass\n'
        self.assertEqual(actual, expected)

    def test_generate_method_stub_duplicate_args_and_kwargs(self):
        actual = self.component.generate_method_stub(
            'persist_evil_dead',
            ['arg1'],
            [('arg1', 'None'), ('arg2', "'Tasty'")]
        )
        actual = actual.replace('    ', '')

        expected = "def persist_evil_dead(self, arg1, arg2='Tasty'):\npass\n"
        self.assertEqual(actual, expected)
