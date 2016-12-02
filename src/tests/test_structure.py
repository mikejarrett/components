# -*- coding: utf-8 -*-o
from unittest import TestCase
import os

from structure import (
    build_client_structure,
    build_logic_structure,
    build_storage_structure,
    create_modules,
    validate_component,
)


class TestStructure(TestCase):

    maxDiff = None
    component_name = 'something_weird'

    def tearDown(self):
        for root, dirs, files in os.walk(self.component_name, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def test_validate_component(self):
        actual = validate_component('sOMETHING wEiRd')
        self.assertEqual(actual, 'Something_Weird')

    def test_validate_component_leading_number(self):
        with self.assertRaises(SystemExit):
            validate_component('1')

    def test_create_modules(self):
        py2 = False
        component = 'Something_Weird'
        create_modules(component)
        build_logic_structure(component, py2)
        build_storage_structure(component, py2)
        build_client_structure(component, py2)

        actual = []
        for (dirpath, dirnames, filenames) in os.walk('./something_weird/'):
            if '__pycache__' in dirpath:
                continue

            for filename in filenames:
                if filename.endswith('pyc'):
                    continue
                actual.append(os.path.join(dirpath, filename))

        expected = [
            './something_weird/__init__.py',
            './something_weird/logic/__init__.py',
            './something_weird/logic/logic.py',
            './something_weird/logic/tests/__init__.py',
            './something_weird/logic/tests/tests.py',
            './something_weird/logic/tests/interface.py',
            './something_weird/clients/fake.py',
            './something_weird/clients/__init__.py',
            './something_weird/clients/tests/__init__.py',
            './something_weird/clients/tests/tests.py',
            './something_weird/clients/tests/interface.py',
            './something_weird/storage/__init__.py',
            './something_weird/storage/pure_memory.py',
            './something_weird/storage/tests/__init__.py',
            './something_weird/storage/tests/tests.py',
            './something_weird/storage/tests/interface.py'
        ]

        self.assertEqual(sorted(actual), sorted(expected))
