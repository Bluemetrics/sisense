from sisense.resource import Resource
from .user import User


class Group(Resource):

    def get(self, name: str = None, oid: str = None) -> Resource:
        """Get group by name. At least one parameter should be set.

        :param name: (str, default None) Group's name.
        :param oid: (str, default None) Group's ID.
        :return: Group, if found. None, otherwise.
        """
        if oid:
            content = self._api.get(f'groups/{oid}')
        elif name:
            content = self._api.get('groups', query={'name': name})
            content = content[0] if len(content) else None
        else:
            raise ValueError('At least one parameter should be set.')

        return Group(self._api, content) if content else None

    def all(self, **kwargs) -> list:
        """
        Get all groups.

        :param kwargs: Positional optional arguments used to filter users:
            - name: (str) Group's name.
            - mail: (str) Group's email.
            - roleId: (str) Role ID.
            - origin: ('ad', 'sisense') User's origin.
            - ids: (list) Groups' IDs.
            - fields: (list) Which fields to return.
            - sort: (str) Field in which the results should be sorted.
            - skip: (int) Number of results to skip from start.
            - limit: (int) Number of results returned.
            - expand: (list) Fields that should be expanded (substitutes their IDs with actual objects).
        :return: (list) of Group objects.
        """
        content = self._api.get('groups', query=kwargs)
        content = [Group(self._api, rjson) for rjson in content]

        return content

    def create(self, name: str) -> Resource:
        """
        Create a new group.

        :param name: (str) Group's name.
        :return: (Group) Newly created group.
        """
        data = {'name': name}
        content = self._api.post('groups', data=data)

        return Group(self._api, content)

    def delete(self):
        """Delete the current group."""
        self._api.delete(f'groups/{self._id}')

    def add_user(self, user: User):
        """
        Add a user to the current group.
        If user is already in the group, do nothing.

        :param user: (User) User to be added.
        """
        groups = user.groups if hasattr(user, 'groups') else []

        if self._id not in groups:
            groups.append(self._id)
            user.update(groups=groups)

    def remove_user(self, user: User):
        """
        Remove a user from the current group.
        If user isn't in the group, do nothing.

        :param user: (User) User to be removed.
        """
        groups = user.groups if hasattr(user, 'groups') else []

        if self._id in groups:
            groups = list(set(groups) - {self._id})
            user.update(groups=groups)
