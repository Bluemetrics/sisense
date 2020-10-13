from sisense import Sisense
import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        with open('tests/api_credentials', 'r') as file:
            host = file.readline().replace('\n', '')
            token = file.readline().replace('\n', '')

        self.sisense = Sisense(host, token)
