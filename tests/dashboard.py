from .test_case import TestCaseV1 as TestCase
from sisense.analysis import Dashboard
import unittest
import json


class DashboardTestCase(TestCase):

    def test_get(self):
        dashboard = self.sisense.dashboard
        sample = dashboard.get(name=self.config['dashboard'])

        self.assertIsInstance(sample, Dashboard)
        self.assertEqual(sample.title, self.config['dashboard'])

        same_sample = dashboard.get(oid=sample.oid)

        self.assertEqual(same_sample.title, sample.title)
        self.assertEqual(same_sample.oid, sample.oid)

        sample = dashboard.get(name='Non existing dashboard')
        self.assertEqual(sample, None)

    def test_exists(self):
        dashboard = self.sisense.dashboard
        sample = dashboard.get(name=self.config['dashboard'])

        self.assertTrue(sample.exists())
        self.assertTrue(dashboard.exists(sample.oid))
        self.assertFalse(dashboard.exists('5f624193993ff1002d46e06d'))

    def test_get_shares(self):
        dashboard = self.sisense.dashboard
        sample = dashboard.get(name=self.config['dashboard'])

        shares = sample.get_shares()
        self.assertEqual(len(shares), 1)

    def test_update(self):
        dashboard = self.sisense.dashboard
        sample = dashboard.get(name=self.config['dashboard'])

        new_title = 'New title'
        sample.update(title=new_title)

        sample = dashboard.get(oid=sample.oid)
        self.assertEqual(sample.title, new_title)

    def create(self):
        with open('tests/support_files/dashboard.dash', 'r') as file:
            rjson = json.load(file)

        dashboard = self.sisense.dashboard.new(rjson)
        new_dash = dashboard.do_import('overwrite')

        same_dash = dashboard.get(oid=new_dash.oid)
        self.assertEqual(same_dash.oid, rjson['oid'])
        self.assertEqual(same_dash.title, rjson['title'])
        self.assertEqual(same_dash.parentFolder, rjson['parentFolder'])

    def delete(self):
        dashboard = self.sisense.dashboard
        sample = dashboard.get(name=self.config['dashboard'])

        if sample:
            sample.delete()

        sample = dashboard.get(name=self.config['dashboard'])
        self.assertEqual(sample, None)


if __name__ == '__main__':
    unittest.main()
