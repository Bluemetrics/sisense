from .data import Datamodel, Build, Permission
from .admin import User, Group
from .api import API


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
    def permission(self) -> Permission:
        """Start point for permission objects."""
        api = self._api_v09()
        return Permission(api)

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

    def _api_v2(self):
        return API(self._host, 'v2', self._token)

    def _api_v1(self):
        return API(self._host, 'v1', self._token)

    def _api_v09(self):
        return API(self._host, '', self._token)
