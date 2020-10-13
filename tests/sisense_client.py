from sisense.data import Datamodel, Build
from sisense import Sisense
import unittest


class SisenseTestCase(unittest.TestCase):

    def setUp(self):
        self.sisense = Sisense('test_host', 'test_token')

    def test_datamodel(self):
        datamodel = self.sisense.datamodel
        self.assertEqual(type(datamodel), Datamodel)

    def test_build(self):
        build = self.sisense.build
        self.assertEqual(type(build), Build)


if __name__ == '__main__':
    unittest.main()
