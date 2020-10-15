from .test_case import TestCase
from time import sleep
import unittest
import requests
import json
import os


class DatamodelTestCase(TestCase):

    def setUp(self):
        super(DatamodelTestCase, self).setUp()
        self.datamodel = self.sisense.datamodel.get(oid='893d2d14-e73c-4864-aced-0f7360c4be85')

    def test_get_by_id(self):
        datamodel = self.datamodel.get(oid='893d2d14-e73c-4864-aced-0f7360c4be85')
        self.assertEqual(datamodel.title, 'SisenseAPI Example')

    def test_get_by_name(self):
        datamodel = self.datamodel.get(title='SisenseAPI Example')
        self.assertEqual(datamodel.oid, '893d2d14-e73c-4864-aced-0f7360c4be85')

    def test_get_builds(self):
        for status in ['pending', 'building', 'done', 'failed', 'cancelled']:
            with self.subTest(status=status):
                builds = self.datamodel.get_builds(status)
                self.assertEqual(type(builds), list)

                for b in builds:
                    self.assertEqual(b.status, status)

    def test_create(self):
        title = 'SisenseAPI (New) Example'
        new_datamodel = self.datamodel.create(title)
        server_datamodel = self.datamodel.get(title=title)

        self.assertEqual(new_datamodel.oid, server_datamodel.oid)
        server_datamodel.delete()

    def test_clone(self):
        title = 'SisenseAPI (Clone) Example'
        new_datamodel = self.datamodel.clone(title)
        server_datamodel = self.datamodel.get(title=title)

        self.assertEqual(new_datamodel.oid, server_datamodel.oid)
        server_datamodel.delete()

    def test_delete(self):
        new_datamodel = self.datamodel.create('SisenseAPI (Delete) Example')
        oid = new_datamodel.oid
        new_datamodel.delete()

        try:
            server_datamodel = self.datamodel.get(oid=oid)
            self.assertIsNone(server_datamodel.oid)
        except requests.exceptions.HTTPError as error:
            self.assertEqual(error.response.status_code, 404)

    def test_export(self):
        with self.subTest(full=False):
            filename = 'datamodel.smodel'
            self.datamodel.export_datamodel(filename, full=False)

            with open(filename, 'r') as file:
                schema = json.load(file)

            self.assertEqual(schema['title'], self.datamodel.title)

            os.system(f'rm {filename}')

        with self.subTest(full=True):
            filename = 'datamodel.sdata'
            self.datamodel.export_datamodel(filename, full=True)
            new_datamodel = self.datamodel.import_datamodel('SisenseAPI (Import) Example', filename, full=True)

            self.assertEqual(type(new_datamodel.oid), str)
            new_datamodel.delete()

            os.system(f'rm {filename}')

    def test_import(self):
        title = 'SisenseAPI (Import) Example'

        with self.subTest(full=False):
            filename = 'datamodel.smodel'
            self.datamodel.export_datamodel(filename, full=False)
            self.datamodel.import_datamodel(title, filename, full=False)

            new_datamodel = self.datamodel.get(title=title)
            self.assertEqual(new_datamodel.title, title)
            self.assertNotEqual(new_datamodel.oid, self.datamodel.oid)

            new_datamodel.delete()
            os.system(f'rm {filename}')

        with self.subTest(full=True):
            filename = 'datamodel.sdata'
            self.datamodel.export_datamodel(filename, full=True)
            new_datamodel = self.datamodel.import_datamodel(title, filename, full=True)

            self.assertEqual(new_datamodel.title, title)
            self.assertNotEqual(new_datamodel.oid, self.datamodel.oid)

            new_datamodel.delete()
            os.system(f'rm {filename}')

    def test_start_build(self):
        build_types = ['full', 'schema_changes', 'by_table']

        for bt in build_types:
            with self.subTest(build_type=bt):
                datamodel = self.datamodel.get(title='ujk3z02fkh_renovation_tracker')
                build = datamodel.start_build(bt)

                self.assertEqual(build.buildType, bt.replace('_', '-'))
                self.assertEqual(build.datamodelId, datamodel.oid)

                while not build.is_finished():
                    sleep(2)
                    build.update()

    def test_stop_builds(self):
        datamodel = self.datamodel.get(title='ujk3z02fkh_renovation_tracker')
        build = datamodel.start_build('full')

        while not build.is_building():
            sleep(2)
            build.update()

        sleep(10)
        build.stop()
        sleep(4)
        self.assertTrue(build.was_cancelled())

    def test_stop_all_builds(self):
        datamodel = self.datamodel.get(title='ujk3z02fkh_renovation_tracker')
        build = datamodel.start_build('full')

        while not build.is_building():
            sleep(2)
            build.update()

        sleep(10)
        datamodel.stop_builds()
        sleep(4)
        build.update()
        self.assertTrue(build.was_cancelled())


if __name__ == '__main__':
    unittest.main()
