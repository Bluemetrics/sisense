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
        self.fix_shares()

    def new(self, rjson: dict) -> object:
        """
        Create a new resource with different properties, but same API.

        :param rjson: (dict) Resource representation.
        :return: (Resource) The new resource
        """
        return self.__class__(self._api, rjson)

    def save(self, filepath: str):
        """
        Save the object representation as a .json file.

        :param filepath: (str) Relative/absolute path, including filename.
        """
        with open(filepath, 'w') as file:
            json.dump(self.json, file)

    def load(self, filepath: str) -> object:
        """
        Load the object representation.

        :param filepath: (str) Relative/absolute path to a .json file.
        """
        with open(filepath, 'r') as file:
            rjson = json.load(file)

        return self.new(rjson)

    def fix_shares(self) -> object:
        """
        When API returns some resource with shares, each share has a field called 'partyId'.
        However, when adding or updating this resource, the API only accepts the field 'party'.
        So, this method replaces 'partyId' with 'party'.

        :return: (Resource) The updated resource.
        """
        if hasattr(self, 'shares'):
            for i, share in enumerate(self.shares):
                if 'partyId' in share:
                    share['party'] = share['partyId']

                share.pop('partyId', None)
                share.pop('partyName', None)

                self.shares[i] = share

        elif hasattr(self, 'partyId'):
            self.json['party'] = self.json['partyId']
            self.json.pop('partyId')

        return self

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
