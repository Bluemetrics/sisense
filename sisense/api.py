from urllib.parse import quote
from .utils import is_json
import requests
import os


class API:

    def __init__(self, host: str, version: str, token: str = None):
        """
        Manage server's requests and responses.

        :param host: (str) Domain name server.
        :param version: (str) API's version. Ex.: 'v1'.
        :param token: (str, default None) API's access token.
        """
        self._host = host
        self._version = version
        self._token = token

        self._url = os.path.join(host, 'api', version)

    @property
    def host(self) -> str:
        """API's domain name server."""
        return self._host

    @property
    def version(self) -> str:
        """API's version."""
        return self._version

    def url(self, uri: str = '') -> str:
        """
        Get API's full URL.

        :param uri: (str, default '') Resource identifier.
        :return: (str) Full url.
        """
        uri = quote(uri)
        return os.path.join(self._url, uri)

    def get(self, uri: str, query: dict = None, headers: dict = None) -> dict:
        """
        Retrieve the specified resource.

        :param uri: (str) Resource identifier.
        :param query: (dict, default None) GET query parameters.
        :param headers: (dict, default None) Request headers.

        :return: (dict) Response
        """
        return self._request('GET', uri, headers=headers, params=query)

    def post(self, uri: str, data: dict = None, query: dict = None, headers: dict = None) -> dict:
        """
        Create a resource in the specified collection.

        :param uri: (str) Resource identifier.
        :param data: (dict, default None) Resource representation as json.
        :param query: (dict, default None) GET query parameters.
        :param headers: (dict, default None) Request headers.

        :return: (dict) Response
        """
        return self._request('POST', uri, headers=headers, json=data, params=query)

    def put(self, uri: str, data: dict = None, headers: dict = None) -> dict:
        """
        Replace the specified resource.

        :param uri: (str) Resource identifier.
        :param data: (dict, default None) Resource representation as json.
        :param headers: (dict, default None) Request headers.

        :return: (dict) Response
        """
        return self._request('PUT', uri, headers=headers, json=data)

    def patch(self, uri: str, data: dict = None, headers: dict = None) -> dict:
        """
        Update the specified resource without replacing it.

        :param uri: (str) Resource identifier.
        :param data: (dict, default None) Resource representation as json.
        :param headers: (dict, default None) Request headers.

        :return: (dict) Response
        """
        return self._request('PATCH', uri, headers=headers, json=data)

    def delete(self, uri: str, query: dict = None, headers: dict = None) -> dict:
        """
        Delete the specified resource.

        :param uri: (str) Resource identifier.
        :param query: (dict, default None) GET query parameters.
        :param headers: (dict, default None) Request headers.

        :return: (dict) Response
        """
        return self._request('DELETE', uri, headers=headers, params=query)

    def download(self, uri: str, filepath: str, query: dict = None, headers: dict = None):
        """
        Download file from stream.

        :param uri: (str) Resource identifier.
        :param filepath: (str) Where to save the downloaded file, including file's name.
        :param query: (dict, default None) GET query parameters.
        :param headers: (dict, default None) Request headers.
        """
        path = self.url(uri)
        headers = self._headers(headers)
        headers.update({'Accept': '*/*'})

        with requests.get(path, params=query, headers=headers, stream=True, verify=False) as response:
            self._handle_request_error(response)

            with open(filepath, 'wb') as file:
                [file.write(chunk) for chunk in response.iter_content(chunk_size=None, decode_unicode=True) if chunk]

    def upload(self, uri: str, file: dict, query: dict = None, headers: dict = None):
        """
        Upload a file.

        :param uri: (str) Resource identifier.
        :param file: (dict) {key: file-like-object File to be uploaded}.
        :param query: (dict, default None) GET query parameters.
        :param headers: (dict, default None) Request headers.
        """
        path = self.url(uri)
        headers = self._headers(headers)
        headers.update({'Accept': '*/*'})
        headers.update({'Content-type': 'multipart/form-data'})

        response = requests.post(path, files=file, params=query, headers=headers, verify=False)
        self._handle_request_error(response)

    def _headers(self, other: dict) -> dict:
        headers = {'authorization': self._token} if self._token else {}

        headers.update(other if other else {})
        headers.update({'Accept': 'application/json'})
        headers.update({'Content-type': 'application/json'})

        return headers

    def _request(self, method: str, uri: str, **kwargs) -> dict:
        requests.packages.urllib3.disable_warnings()

        path = self.url(uri)
        kwargs['headers'] = self._headers(kwargs['headers'])
        kwargs['verify'] = False

        response = requests.request(method, path, **kwargs)
        self._handle_request_error(response)

        if len(response.text):
            content = response.json() if is_json(response.text) else {'message': response.text}
        else:
            content = {}

        return content

    def _handle_request_error(self, response):
        response.raise_for_status()

    # TODO: keep requests log
