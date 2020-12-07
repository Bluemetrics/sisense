from sisense.data import Datamodel, Build, Permission
from .test_case import TestCaseV2 as TestCase
from sisense.admin import User, Group
import unittest


class SisenseTestCase(TestCase):

    def test_datamodel(self):
        obj = self.sisense.datamodel
        self.assertEqual(type(obj), Datamodel)

    def test_build(self):
        obj = self.sisense.build
        self.assertEqual(type(obj), Build)

    def test_permission(self):
        obj = self.sisense.permission
        self.assertEqual(type(obj), Permission)

    def test_user(self):
        obj = self.sisense.user
        self.assertEqual(type(obj), User)

    def test_group(self):
        obj = self.sisense.group
        self.assertEqual(type(obj), Group)


if __name__ == '__main__':
    unittest.main()
