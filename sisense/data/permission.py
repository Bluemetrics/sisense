from sisense.resource import Resource


class Permission(Resource):

    def get(self, elasticube: str) -> list:
        """Get permissions (shares) for the specified elasticube.

        :param elasticube: (str) Elasticube's name.
        :return: a list of permission objects
        """
        content = self._api.get(f'elasticubes/localhost/{elasticube}/permissions')

        permissions = []
        for p in content['shares']:
            p['party'] = p['partyId']
            del p['partyId']

            permissions.append(Permission(self._api, p))

        return permissions

    def add(self, elasticube: str, oid: str = None, ptype: str = None, permission: str = None) -> object:
        """Add new permissions to the specified elasticube.
        If any optional parameters are None, add the current permission.

        :param elasticube: (str, default None) Elasticube's name.
        :param oid: (str, default None) Group/user id.
        :param ptype: (str, default None) Party's type. Possible values are: 'group' or 'user'.
        :param permission: (str, default None) Permission's type. Possible values are: 'r' (read) or 'w' (write).
        :return: Permission
        """
        if oid is None or type is None or permission is None:
            data = [self._json]
        else:
            data = [{'party': oid, 'type': ptype, 'permission': permission}]

        self._api.put(f'elasticubes/localhost/{elasticube}/permissions', data=data)

        return Permission(self._api, data[0])

    def delete_all(self, elasticube: str):
        """Delete all elasticube's permissions.

        :param elasticube: (str, default None) Elasticube's name.
        """
        self._api.delete(f'elasticubes/localhost/{elasticube}/permissions')
