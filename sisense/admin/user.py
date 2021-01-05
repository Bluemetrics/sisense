from sisense.resource import Resource


class User(Resource):

    def get(self, email: str = None, oid: str = None) -> Resource:
        """Get user by e-mail. At least one parameter should be set.

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

    def create(self, email: str, **kwargs) -> Resource:
        """
        Create a new user.

        :param email: (str) User's email.
        :param kwargs: (dict) Optional keyword arguments:
            - userName: (str) Username.
            - firstName: (str) First name.
            - lastName: (str) Last name.
            - roleId: (str) Role's ID.
            - groups: (list) Group's ID in which user is part of.
        :return: (User) Newly created user.
        """
        data = {'email': email}
        data.update(kwargs)

        content = self._api.post('users', data=data)
        return User(self._api, content)

    def delete(self):
        """Delete the current user."""
        self._api.delete(f'users/{self._id}')
