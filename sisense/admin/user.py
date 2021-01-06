from sisense.resource import Resource


class User(Resource):

    def get(self, email: str = None, oid: str = None) -> Resource:
        """
        Get user by e-mail. At least one parameter should be set.

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

    def all(self, **kwargs) -> list:
        """
        Get all users.

        :param kwargs: Positional optional arguments used to filter users:
            - userName: (str) Username.
            - email: (str) User's email.
            - firstName: (str) User's first name.
            - lastName: (str) User's last name.
            - roleId: (str) Role ID.
            - groupId: (str) Group ID.
            - active: (bool) Whether to get active users (True) or not (False).
            - origin: ('ad', 'sisense') User's origin.
            - ids: (list) Users' IDs.
            - fields: (list) Which fields to return.
            - sort: (str) Field in which the results should be sorted.
            - skip: (int) Number of results to skip from start.
            - limit: (int) Number of results returned.
            - expand: (list) Fields that should be expanded (substitutes their IDs with actual objects).
        :return: (list)
        """
        content = self._api.get('users', query=kwargs)
        content = [User(self._api, rjson) for rjson in content]

        return content

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

    def update(self, **kwargs):
        """
        Update the current user.

        At least one argument must be set.

        :param kwargs: Positional optional arguments:
            - email: (str),
            - userName: (str) Username.
            - firstName: (str) First name.
            - lastName: (str) Last name.
            - roleId: (str) Role's ID.
            - groups: (list) Group's ID in which user is part of.
            - preferences: (dict) User's preferences such as 'localeId'.
            - uiSettings: (dict) User's UI settings.
        """
        content = self._api.patch(f'users/{self._id}', data=kwargs)
        self.json = content

    def delete(self):
        """Delete the current user."""
        self._api.delete(f'users/{self._id}')
