from .api import API
import json


class Resource:

    def __init__(self, api: API, rjson: dict = None):
        """
        Super for any API's resource.

        :param api: (API) Used to make API's requests.
        :param rjson: (dict) Resource representation.
        """
        # If you add a new attribute, always remember to include it on __setattr__
        self._api = api
        self.json = rjson if rjson else {}

    def new(self, rjson: dict) -> object:
        """Create a new resource with different properties, but same API.

        :param rjson: (dict) Resource representation.
        :return: (Resource) The new resource
        """
        return Resource(self._api, rjson)

    def save(self, filepath: str):
        """
        Save the object representation as a .json file.

        :param filepath: (str) Relative/absolute path, including filename.
        """
        filepath = filepath if filepath.endswith('.json') else f'{filepath}.json'
        with open(filepath, 'r') as file:
            json.dump(self.json, file)

    def __setattr__(self, key, value):
        if key in self.__dict__ or key in ['json', '_api', '_elasticube']:
            self.__dict__[key] = value
        else:
            self.__dict__['json'][key] = value

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self.__dict__['json']:
            return self.__dict__['json'][item]

        raise AttributeError(f'"{item}" does not exist in {type(self)}.')

    def __repr__(self):
        return str(self.json)
