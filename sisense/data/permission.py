from sisense.resource import Resource
from sisense.api import API


class Permission(Resource):

    def __init__(self, api: API, rjson: dict = None, elasticube_name: str = None):
        super().__init__(api, rjson)
        self._elasticube = elasticube_name

    def all(self, elasticube: str = None) -> list:
        """
        Get permissions (shares) for the specified elasticube.

        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.
        :return: a list of permission objects
        """
        elasticube = elasticube if elasticube else self._elasticube
        content = self._api.get(f'elasticubes/localhost/{elasticube}/permissions')

        if 'shares' in content:
            permissions = [Permission(self._api, share, elasticube) for share in content['shares']]
        else:
            permissions = []

        return list(permissions)

    def get(self, oid: str, elasticube: str = None) -> Resource:
        """
        Get the permission for a user/group.

        :param oid: (str) Party ID.
        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.
        :return: (Permission) if found. None, otherwise.
        """
        for share in self.all(elasticube):
            if share.party == oid:
                return share

        return None

    def create(self, oid: str = None, ptype: str = None, level: str = None, elasticube: str = None) -> Resource:
        """
        Create new permission to the specified elasticube.
        If any optional parameters are None, add the current permission.

        :param oid: (str, default None) Group/user id.
        :param ptype: (str, default None) Party's type. Possible values are: 'group' or 'user'.
        :param level: (str, default None) Permission's type. Possible values are: 'r' (read) or 'w' (write).
        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.

        :return: (Permission) The new permission.
        """
        elasticube = elasticube if elasticube else self._elasticube
        data = self.json if oid is None or type is None or level is None else {'party': oid,
                                                                               'type': ptype,
                                                                               'permission': level}

        permissions = [share.json for share in self.all(elasticube)] + [data]
        self._api.put(f'elasticubes/localhost/{elasticube}/permissions', data=permissions)

        return Permission(self._api, data, elasticube)

    def delete(self):
        """Delete the current permission."""
        permissions = self.all()
        self._api.delete(f'elasticubes/localhost/{self._elasticube}/permissions')
        [share.create(share.party, share.type, share.permission) for share in permissions if share.party != self.party]

    def delete_all(self, elasticube: str = None):
        """
        Delete all elasticube's permissions.

        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.
        """
        elasticube = elasticube if elasticube else self._elasticube
        self._api.delete(f'elasticubes/localhost/{elasticube}/permissions')
