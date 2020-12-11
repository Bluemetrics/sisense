from .test_case import TestCaseV09 as TestCase
from sisense.data import Hierarchy
import unittest


class HierarchyTestCase(TestCase):

    def test_get(self):
        hierarchy = self.sisense.hierarchy
        results = hierarchy.get(self.config['elasticube'])

        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0].levels), 2)
        self.assertEqual(results[0].title, 'Category > Product')

        for h in hierarchy:
            self.assertEqual(type(h), Hierarchy)

    def test_add(self):
        hierarchy = self.sisense.hierarchy
        results = hierarchy.get(self.config['elasticube'])
        old_hierarchy = results[0]

        old_hierarchy.title = 'Category > Product (Copy)'

        new_hierarchy = hierarchy.add(self.config['elasticube'], old_hierarchy)
        new_results = hierarchy.get(self.config['elasticube'])
        new_hierarchy.delete()

        self.assertEqual(len(results) + 1, len(new_results))

        for h in new_results:
            self.assertEqual(len(h.levels), 2)
            self.assertTrue('Category > Product' in h.title)
            self.assertEqual(type(h), Hierarchy)

    def test_delete(self):
        hierarchy = self.sisense.hierarchy
        results = hierarchy.get(self.config['elasticube'])
        original = results[0]

        title = 'Category > Product (Copy)'

        for i in range(5):
            new_title = f'{title} {i}'
            original.title = new_title
            original.add()

        results = hierarchy.get(self.config['elasticube'])
        self.assertEqual(len(results), 6)

        for h in results:
            if h._id != original._id:
                h.delete()

        results = hierarchy.get(self.config['elasticube'])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]._id, original._id)


if __name__ == '__main__':
    unittest.main()
