from sisense.api import API


class AuthModel:

    def __init__(self, host: str, username: str, password: str):
        """
        Authentication model for Sisense API.

        :param host: (str) Domain name server.
        :param username: (str) User's login name.
        :param password: (str) User's password.
        """
        self._token = ''
        self._api = API(host, 'v1')

        self.login(username, password)

    @property
    def token(self) -> str:
        """
        Get access token.

        :return: (str)
        """
        return f"Bearer {self._token}"

    def login(self, username: str, password: str):
        """
        Get an access token using the specified credentials.

        :param username: (str) User's login name.
        :param password: (str) User's password.
        """
        raise NotImplementedError

    def logout(self):
        """Revoke access token."""
        raise NotImplementedError

    def is_logged(self) -> bool:
        """True, if user is logged. False, otherwise."""
        return bool(len(self._token))

    def _reset_token(self):
        self._token = ''

    def __del__(self):
        self.logout()
