from sisense.resource import Resource


class User(Resource):

    def get(self, email: str) -> object:
        """Get user by e-mail.

        :param email: (str) User's e-mail.
        :return: User, if found. None, otherwise.
        """
        content = self._api.get('users', query={'email': email})
        return User(self._api, content[0]) if len(content) else None
