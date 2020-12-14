from .test_case import TestCaseV09 as TestCase
from sisense.data import DataSecurity
import unittest


class DataSecurityTestCase(TestCase):

    def test_get(self):
        results = self.sisense.datasecurity.get(self.config['elasticube'])

        self.assertEqual(len(results), 4)
        self.assertIsInstance(results, list)

        for ds in results:
            self.assertIsInstance(ds, DataSecurity)

    def test_add(self):
        results = self.sisense.datasecurity.get(self.config['elasticube'])

        results[1].exclusionary = True
        ds = self.sisense.datasecurity.add(self.config['elasticube'], results[1])

        new_results = self.sisense.datasecurity.get(self.config['elasticube'])
        ds.delete()

        self.assertEqual(len(results) + 1, len(new_results))

    def test_update(self):
        results = self.sisense.datasecurity.get(self.config['elasticube'])

        datasecurity = None
        for ds in results:
            if 'Mississippi' in ds.members:
                datasecurity = ds
                break

        datasecurity.members.append('California')

        new_datasecurity = datasecurity.update(datasecurity)
        new_results = self.sisense.datasecurity.get(self.config['elasticube'])

        self.assertEqual(len(new_datasecurity.members), len(datasecurity.members))
        self.assertEqual(len(results), len(new_results))
        self.assertIn('California', new_datasecurity.members)

        datasecurity.members = ['Mississippi']
        datasecurity.update(datasecurity)

    def test_delete(self):
        results = self.sisense.datasecurity.get(self.config['elasticube'])

        i = 1
        for ds in results:
            ds.delete()
            new_results = self.sisense.datasecurity.get(self.config['elasticube'])

            self.assertEqual(len(results), len(new_results) + i)
            i = i + 1

        new_results = self.sisense.datasecurity.get(self.config['elasticube'])

        self.assertEqual(len(new_results), 0)

        for ds in results:
            ds.add(self.config['elasticube'])


if __name__ == '__main__':
    unittest.main()
