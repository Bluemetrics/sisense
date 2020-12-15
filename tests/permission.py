from .test_case import TestCaseV09 as TestCase
from sisense.data import Permission
import unittest
import json


class PermissionTestCase(TestCase):

    def test_all(self):
        results = self.sisense.permission.all(elasticube=self.config['elasticube'])
        ids = [p.party for p in self.permissions]

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), len(self.permissions))

        for p in results:
            self.assertIsInstance(p, Permission)
            self.assertIn(p.party, ids)

    def test_get(self):
        p = self.sisense.permission.get(self.permissions[-1].party, self.config['elasticube'])

        self.assertIsInstance(p, Permission)
        self.assertEqual(p.party, self.permissions[-1].party)

    def test_delete(self):
        permission = self.sisense.permission

        p = permission.get(self.permissions[-1].party, self.config['elasticube'])
        p.delete()

        results = permission.all(self.config['elasticube'])
        ids = [p.party for p in results]

        self.assertEqual(len(results), len(self.permissions) - 1)
        self.assertNotIn(p.party, ids)

    def create(self):
        permission = self.sisense.permission

        with open('tests/support_files/permission.json', 'r') as file:
            permissions = json.load(file)

        for p in permissions:
            permission.create(p['party'], p['type'], p['permission'], self.config['elasticube'])

        self.permissions = permission.all(elasticube=self.config['elasticube'])
        self.assertEqual(len(self.permissions), len(permissions))

    def delete(self):
        permission = self.sisense.permission
        permission.delete_all(self.config['elasticube'])

        results = permission.all(self.config['elasticube'])
        self.assertEqual(len(results), 1)


if __name__ == '__main__':
    unittest.main()
