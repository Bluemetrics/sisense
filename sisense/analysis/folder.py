from sisense.resource import Resource


class Folder(Resource):

    def get(self, oid: str) -> Resource:
        """
        Get a specific folder.

        :param oid: (str) Folder's ID.
        :return: (Folder)
        """
        content = self._api.get(f'folders/{oid}')
        return Folder(self._api, content)

    def get_all(self) -> list:
        """Get all folders.
        :return: (list) List of folder objects.
        """
        content = self._api.get('folders')
        results = [Folder(self._api, rjson) for rjson in content]
        return results
