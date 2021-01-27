from .test_case import TestCaseV1 as TestCase
from sisense.data import Elasticube
import unittest


class ElasticubeTestCase(TestCase):

    def test_all(self):
        results = self.sisense.elasticube.all()

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        for cube in results:
            self.assertIsInstance(cube, Elasticube)

    def test_get(self):
        cube = self.sisense.elasticube.get(self.config['elasticube'])

        self.assertIsInstance(cube, Elasticube)
        self.assertEqual(cube.title, self.config['elasticube'])


if __name__ == '__main__':
    unittest.main()
