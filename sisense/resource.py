from .api import API
import json


class Resource:

    def __init__(self, api: API, rjson: dict = None):
        """
        Super for any API's resource.

        :param api: (API) Used to make API's requests.
        :param rjson: (dict) Resource representation.
        """
        self._api = api
        self._json = rjson if rjson else {}

    @property
    def json(self) -> dict:
        return self._json

    @json.setter
    def json(self, other):
        self._json = dict(other)

    def save(self, filepath: str):
        """
        Save the object representation as a .json file.

        :param filepath: (str) Relative/absolute path, including filename.
        """
        filepath = filepath if filepath.endswith('.json') else f'{filepath}.json'
        with open(filepath, 'r') as file:
            json.dump(self.json, file)

    def __setattr__(self, key, value):
        self._json[key] = value

    def __getattr__(self, item):
        return self._json.get(item, None)

    def __repr__(self):
        return str(self.json)
