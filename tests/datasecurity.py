from .test_case import TestCaseV09 as TestCase
from sisense.data import DataSecurity
import unittest
import json


class DataSecurityTestCase(TestCase):

    def test_all(self):
        datasecurity = self.sisense.datasecurity

        results = datasecurity.all(elasticube=self.config['elasticube'])
        ids = [r._id for r in self.rules]

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), len(self.rules))

        for rule in results:
            self.assertIsInstance(rule, DataSecurity)
            self.assertIn(rule._id, ids)

        results = datasecurity.all(self.rules[-1].table, self.rules[-1].column, self.config['elasticube'])
        for rule in results:
            self.assertEqual(self.rules[-1].table, rule.table)
            self.assertEqual(self.rules[-1].column, rule.column)

    def test_get(self):
        rule = self.sisense.datasecurity.get(self.rules[0]._id, self.config['elasticube'])

        self.assertIsInstance(rule, DataSecurity)
        self.assertEqual(rule._id, self.rules[0]._id)

    def test_update(self):
        for r in self.rules:
            if hasattr(r, 'members') and len(r.members):
                rule = r
                break

        rule.exclusionary = True
        rule.members.append('California')

        new_rule = rule.update()

        self.assertTrue(new_rule.exclusionary)
        self.assertEqual(len(new_rule.members), len(rule.members))
        self.assertIn('California', new_rule.members)

    def test_delete_all(self):
        datasecurity = self.sisense.datasecurity

        datasecurity.delete_all('DimProducts', 'ProductName', self.config['elasticube'])
        this_results = datasecurity.all('DimProducts', 'ProductName', elasticube=self.config['elasticube'])
        other_results = datasecurity.all(elasticube=self.config['elasticube'])

        self.assertEqual(len(this_results), 0)
        self.assertNotEqual(len(other_results), len(self.rules))

    def create(self):
        datasecurity = self.sisense.datasecurity

        with open('tests/support_files/datasecurity.json', 'r') as file:
            rules = json.load(file)

        for rule in rules:
            rule.pop('elasticube', None)
            datasecurity.create(**rule, elasticube=self.config['elasticube'])

        self.rules = datasecurity.all(elasticube=self.config['elasticube'])
        self.assertEqual(len(self.rules), len(rules))

    def delete(self):
        datasecurity = self.sisense.datasecurity
        results = datasecurity.all(elasticube=self.config['elasticube'])
        [rule.delete() for rule in results]

        new_results = datasecurity.all(elasticube=self.config['elasticube'])
        self.assertEqual(len(new_results), 0)


if __name__ == '__main__':
    unittest.main()
