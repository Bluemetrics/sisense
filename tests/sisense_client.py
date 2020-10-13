from sisense.data import Datamodel, Build
from .test_case import TestCase
import unittest


class SisenseTestCase(TestCase):

    def test_datamodel(self):
        datamodel = self.sisense.datamodel
        self.assertEqual(type(datamodel), Datamodel)

    def test_build(self):
        build = self.sisense.build
        self.assertEqual(type(build), Build)


if __name__ == '__main__':
    unittest.main()
