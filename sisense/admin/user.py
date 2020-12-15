from sisense.resource import Resource


class User(Resource):

    def get(self, email: str = None, oid: str = None) -> object:
        """Get user by e-mail.
        At least one parameter should be set.

        :param email: (str, default None) User's e-mail.
        :param oid: (str, default None) User's ID.
        :return: User, if found. None, otherwise.
        """
        if oid:
            content = self._api.get(f'users/{oid}')
        elif email:
            content = self._api.get('users', query={'email': email})
            content = content[0] if len(content) else None
        else:
            raise ValueError('At least one parameter should be set.')

        return User(self._api, content) if content else None
