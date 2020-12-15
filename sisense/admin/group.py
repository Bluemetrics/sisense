from sisense.resource import Resource


class Group(Resource):

    def get(self, name: str = None, oid: str = None) -> object:
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
