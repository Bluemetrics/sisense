from sisense.resource import Resource


class Group(Resource):

    def get(self, name: str) -> object:
        """Get group by name.

        :param name: (str) Group's name.
        :return: Group, if found. None, otherwise.
        """
        content = self._api.get('groups', query={'name': name})
        return Group(self._api, content[0]) if len(content) else None
