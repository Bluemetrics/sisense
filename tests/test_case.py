from sisense import Sisense
import unittest
import json


def _load_config(version: str) -> dict:
    with open(f'tests/support_files/config/api_{version}.json', 'r') as file:
        return json.load(file)


class TestCase(unittest.TestCase):

    def create(self):
        pass

    def delete(self):
        pass

    def setUp(self) -> None:
        super().setUp()
        self.delete()
        self.create()

    def tearDown(self) -> None:
        super().tearDown()
        self.delete()


class TestCaseV09(TestCase):

    def setUp(self):
        self.config = _load_config('v09')
        self.sisense = Sisense(self.config['host'], self.config['token'])

        super().setUp()


class TestCaseV1(TestCase):

    def setUp(self):
        self.config = _load_config('v1')
        self.sisense = Sisense(self.config['host'], self.config['token'])

        super().setUp()


class TestCaseV2(TestCase):

    def setUp(self):
        self.config = _load_config('v2')
        self.sisense = Sisense(self.config['host'], self.config['token'])

        super().setUp()
