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

    def add(self, elasticube: str, oid: str = None, ptype: str = None, level: str = None, permissions: list = None):
        """Add new permissions to the specified elasticube.
        If permissions is none and any other optional parameters are None, add the current permission.
        Use permissions parameter to add several permissions at once.
        Use the other parameters to add just one permission.

        :param elasticube: (str, default None) Elasticube's name.
        :param oid: (str, default None) Group/user id.
        :param ptype: (str, default None) Party's type. Possible values are: 'group' or 'user'.
        :param level: (str, default None) Permission's type. Possible values are: 'r' (read) or 'w' (write).
        :param permissions: (list) List of permissions JSONs to add all at once.
        """
        if permissions is None:
            if oid is None or type is None or level is None:
                data = [self._json]
            else:
                data = [{'party': oid, 'type': ptype, 'permission': level}]
        else:
            data = permissions

        all_permissions = self.get(elasticube)
        all_permissions = [p.json for p in all_permissions] + data

        self._api.put(f'elasticubes/localhost/{elasticube}/permissions', data=all_permissions)

    def delete_all(self, elasticube: str):
        """Delete all elasticube's permissions.

        :param elasticube: (str, default None) Elasticube's name.
        """
        self._api.delete(f'elasticubes/localhost/{elasticube}/permissions')
