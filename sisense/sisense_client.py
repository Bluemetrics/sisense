from .api import API
from .analysis import *
from .admin import *
from .data import *


class Sisense:

    def __init__(self, host: str, token: str):
        """
        Manage API's entities.

        :param host: (str) Domain name server.
        :param token: (str) API's access token.
        """
        self._host = host
        self._token = token if token.startswith('Bearer ') else f'Bearer {token}'

    @property
    def datamodel(self) -> Datamodel:
        """Start point for datamodel objects."""
        api = self._api_v2()
        return Datamodel(api)

    @property
    def build(self) -> Build:
        """Start point for build objects."""
        api = self._api_v2()
        return Build(api)

    @property
    def elasticube(self) -> Elasticube:
        """Start point for elasticube objects."""
        api = self._api_v1()
        return Elasticube(api)

    @property
    def connection(self) -> Connection:
        """Start point for connection objects."""
        api = self._api_v1()
        return Connection(api)

    @property
    def permission(self) -> Permission:
        """Start point for permission objects."""
        api = self._api_v09()
        return Permission(api)

    @property
    def hierarchy(self) -> Hierarchy:
        """Start point for hierarchy objects."""
        api = self._api_v09()
        return Hierarchy(api)

    @property
    def datasecurity(self) -> DataSecurity:
        """Start point for datasecurity objects."""
        api = self._api_v09()
        return DataSecurity(api)

    @property
    def user(self) -> User:
        """Start point for user objects."""
        api = self._api_v1()
        return User(api)

    @property
    def group(self) -> Group:
        """Start point for group objects."""
        api = self._api_v1()
        return Group(api)

    @property
    def dashboard(self) -> Dashboard:
        """Start point for dashboard objects."""
        api = self._api_v1()
        return Dashboard(api)

    @property
    def folder(self) -> Folder:
        """Start point for folder objects."""
        api = self._api_v1()
        return Folder(api)

    def _api_v2(self):
        return API(self._host, 'v2', self._token)

    def _api_v1(self):
        return API(self._host, 'v1', self._token)

    def _api_v09(self):
        return API(self._host, '', self._token)
