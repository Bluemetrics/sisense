from sisense import Sisense
import unittest
import json


def _load_config(version: str) -> dict:
    with open(f'tests/support_files/config/api_{version}.json', 'r') as file:
        return json.load(file)


class TestCaseV09(unittest.TestCase):

    def setUp(self):
        self.config = _load_config('v09')
        self.sisense = Sisense(self.config['host'], self.config['token'])


class TestCaseV1(unittest.TestCase):

    def setUp(self):
        self.config = _load_config('v1')
        self.sisense = Sisense(self.config['host'], self.config['token'])


class TestCaseV2(unittest.TestCase):

    def setUp(self):
        self.config = _load_config('v2')
        self.sisense = Sisense(self.config['host'], self.config['token'])
