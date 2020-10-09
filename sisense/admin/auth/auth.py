from .auth_model import AuthModel


class Auth(AuthModel):

    def login(self, username: str, password: str):
        self.logout()

        data = {'username': username, 'password': password}
        response = self._api.post('authentication/login', data)

        self._token = response['access_token']

    def logout(self):
        if self.is_logged():
            self._api.get('authentication/logout', headers={'authorization': self.token})
            self._reset_token()
