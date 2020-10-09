from .auth_model import AuthModel


class OAuth(AuthModel):

    def login(self, username: str, password: str):
        raise NotImplementedError  # TODO: implement login

    def logout(self):
        raise NotImplementedError  # TODO: implement logout
