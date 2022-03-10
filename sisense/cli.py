from .resource import Resource
from .api import API


class CLI(Resource):

    def __init__(self, api: API, rjson: dict = None):
        """
        Super for any API's resource.

        :param api: (API) Used to make API's requests.
        :param rjson: (dict) Resource representation.
        """
        super(CLI, self).__init__(api, rjson)
        self._uri = 'cli/execute'

    @property
    def uri(self):
        return self._uri

    def execute(self, command: str):
        """
        Execute a command in the CLI.

        :param command: (str) Command without the "si" method. See https://documentation.sisense.com/docs/using-cli-commands.
        :return: (str) Content of the call
        """
        return self._api.post(self.uri, data=command, headers={'Content-type': 'text/plain', 'Accept': '*/*'})
