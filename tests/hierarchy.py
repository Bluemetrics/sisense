from .test_case import TestCaseV09 as TestCase
from sisense.data import Hierarchy
import unittest
import json


class HierarchyTestCase(TestCase):

    def test_all(self):
        results = self.sisense.hierarchy.all(elasticube=self.config['elasticube'])
        ids = [h._id for h in self.hierarchies]

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), len(self.hierarchies))

        for h in results:
            self.assertIsInstance(h, Hierarchy)
            self.assertIn(h._id, ids)

    def test_get(self):
        h = self.sisense.hierarchy.get(self.hierarchies[0]._id, self.config['elasticube'])

        self.assertIsInstance(h, Hierarchy)
        self.assertEqual(h._id, self.hierarchies[0]._id)

    def create(self):
        hierarchy = self.sisense.hierarchy

        with open('tests/support_files/hierarchy.json', 'r') as file:
            hierarchies = json.load(file)

        for h in hierarchies:
            hierarchy.create(h['title'], h['levels'], h['alwaysIncluded'], self.config['elasticube'])

        self.hierarchies = hierarchy.all(self.config['elasticube'])
        self.assertEqual(len(self.hierarchies), len(hierarchies))

    def delete(self):
        hierarchy = self.sisense.hierarchy
        hierarchies = hierarchy.all(self.config['elasticube'])
        [hierarchy.delete() for hierarchy in hierarchies]

        results = hierarchy.all(self.config['elasticube'])
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
