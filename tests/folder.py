from .test_case import TestCaseV1 as TestCase
from sisense.analysis import Folder
import unittest


class FolderTestCase(TestCase):

    def test_get(self):
        folder = self.sisense.folder
        results = folder.all()

        oid = results[0].oid

        one_result = folder.get(oid)
        self.assertIsInstance(one_result, Folder)
        self.assertEqual(one_result.oid, oid)
        self.assertEqual(one_result.name, results[0].name)

    def test_all(self):
        folder = self.sisense.folder
        results = folder.all()

        self.assertGreater(len(results), 1)

        for f in results:
            self.assertIsInstance(f, Folder)

    def create(self):
        folder = self.sisense.folder
        n_folders = len(folder.all())

        parent = folder.create(self.config['folder'])
        child = folder.create(self.config['folder'] + ' Child', parent.oid)

        folders = folder.all()

        self.assertEqual(n_folders + 2, len(folders))
        self.assertEqual(parent.name, self.config['folder'])
        self.assertEqual(child.parentId, parent.oid)

    def delete(self):
        folders = self.sisense.folder.all()

        i = 0
        for folder in folders:
            if folder.name == self.config['folder']:
                folder.delete()
                i = i + 2

        new_folders = self.sisense.folder.all()
        self.assertEqual(len(folders) - i, len(new_folders))


if __name__ == '__main__':
    unittest.main()
