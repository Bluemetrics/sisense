from .test_case import TestCaseV1 as TestCase
from sisense.analysis import Folder
import unittest


class FolderTestCase(TestCase):

    def test_get(self):
        folder = self.sisense.folder
        results = folder.get_all()

        oid = results[0].oid

        one_result = folder.get(oid)
        self.assertIsInstance(one_result, Folder)
        self.assertEqual(one_result.oid, oid)
        self.assertEqual(one_result.name, results[0].name)

    def test_get_all(self):
        folder = self.sisense.folder
        results = folder.get_all()

        for f in results:
            self.assertIsInstance(f, Folder)


if __name__ == '__main__':
    unittest.main()
