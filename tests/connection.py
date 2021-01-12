from .test_case import TestCaseV1 as TestCase
from sisense.data import Connection
import unittest


class ConnectionTestCase(TestCase):

    def test_all(self):
        connections = self.sisense.connection.all(limit=10)

        self.assertEqual(len(connections), 10)

        for conn in connections:
            self.assertIsInstance(conn, Connection)

    def test_get(self):
        connection = self.sisense.connection.all(limit=1)[0]
        other_conn = self.sisense.connection.get(connection._id)

        self.assertEqual(connection._id, other_conn._id)

    def test_update(self):
        parameters = self.conn.parameters
        parameters['IsLive'] = 'false'

        updated_conn = self.conn.update(parameters=parameters)

        self.assertNotEqual(self.conn.parameters['IsLive'], updated_conn.parameters['IsLive'])

    def create(self):
        self.conn = self.sisense.connection.create(provider='Excel', parameters={'filesToImport': 'No existing file.txt'})

        self.assertEqual(self.conn.provider, 'Excel')
        self.assertTrue('filesToImport' in self.conn.parameters)

    def delete(self):
        if hasattr(self, 'conn'):
            self.conn.delete()


if __name__ == '__main__':
    unittest.main()
