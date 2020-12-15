from .test_case import TestCaseV2 as TestCase
import unittest
import requests
import json
import os

# TODO: change unit tests
class DatamodelTestCase(TestCase):
    pass
    # def setUp(self):
    #     super(DatamodelTestCase, self).setUp()
    #     self.datamodel = self.sisense.datamodel.all(oid=self.config['datamodel.oid'])
    #
    # def test_get_by_id(self):
    #     self.assertEqual(self.datamodel.title, self.config['datamodel'])
    #
    # def test_get_by_name(self):
    #     datamodel = self.datamodel.all(title=self.config['datamodel'])
    #     self.assertEqual(datamodel.oid, self.config['datamodel.oid'])
    #
    # def test_create(self):
    #     title = 'SisenseAPI (New) Example'
    #     new_datamodel = self.datamodel.create(title)
    #     server_datamodel = self.datamodel.all(title=title)
    #
    #     self.assertEqual(new_datamodel.oid, server_datamodel.oid)
    #     server_datamodel.delete()
    #
    # def test_clone(self):
    #     title = 'SisenseAPI (Clone) Example'
    #     new_datamodel = self.datamodel.clone(title)
    #     server_datamodel = self.datamodel.all(title=title)
    #
    #     self.assertEqual(new_datamodel.oid, server_datamodel.oid)
    #     server_datamodel.delete()
    #
    # def test_delete(self):
    #     new_datamodel = self.datamodel.create('SisenseAPI (Delete) Example')
    #     oid = new_datamodel.oid
    #     new_datamodel.delete()
    #
    #     try:
    #         server_datamodel = self.datamodel.all(oid=oid)
    #         self.assertIsNone(server_datamodel.oid)
    #     except requests.exceptions.HTTPError as error:
    #         self.assertEqual(error.response.status_code, 404)
    #
    # def test_export(self):
    #     with self.subTest(full=False):
    #         filename = 'datamodel.smodel'
    #         self.datamodel.export_datamodel(filename, full=False)
    #
    #         with open(filename, 'r') as file:
    #             schema = json.load(file)
    #
    #         self.assertEqual(schema['title'], self.datamodel.title)
    #
    #         os.system(f'rm {filename}')
    #
    #     with self.subTest(full=True):
    #         filename = 'datamodel.sdata'
    #         self.datamodel.export_datamodel(filename, full=True)
    #         new_datamodel = self.datamodel.import_datamodel('SisenseAPI (Import) Example', filename, full=True)
    #
    #         self.assertEqual(type(new_datamodel.oid), str)
    #         new_datamodel.delete()
    #
    #         os.system(f'rm {filename}')
    #
    # def test_import(self):
    #     title = 'SisenseAPI (Import) Example'
    #
    #     with self.subTest(full=False):
    #         filename = 'datamodel.smodel'
    #         self.datamodel.export_datamodel(filename, full=False)
    #         self.datamodel.import_datamodel(title, filename, full=False)
    #
    #         new_datamodel = self.datamodel.all(title=title)
    #         self.assertEqual(new_datamodel.title, title)
    #         self.assertNotEqual(new_datamodel.oid, self.datamodel.oid)
    #
    #         new_datamodel.delete()
    #         os.system(f'rm {filename}')
    #
    #     with self.subTest(full=True):
    #         filename = 'datamodel.sdata'
    #         self.datamodel.export_datamodel(filename, full=True)
    #         new_datamodel = self.datamodel.import_datamodel(title, filename, full=True)
    #
    #         self.assertEqual(new_datamodel.title, title)
    #         self.assertNotEqual(new_datamodel.oid, self.datamodel.oid)
    #
    #         new_datamodel.delete()
    #         os.system(f'rm {filename}')


if __name__ == '__main__':
    unittest.main()
