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

    def all(self) -> list:
        """
        Get all folders.

        :return: (list) List of folder objects.
        """
        content = self._api.get('folders')
        results = [Folder(self._api, rjson) for rjson in content]
        return results

    def create(self, name: str, parent: str = None) -> Resource:
        """
        Create a new folder.

        :param name: (str) Folder's name.
        :param parent: (str, default None) Parent folder's ID.
        :return: (Folder) The new folder.
        """
        data = {'name': name}
        if parent:
            data['parentId'] = parent

        content = self._api.post('folders', data=data)
        return Folder(self._api, content)

    def delete(self):
        """Delete the current folder."""
        self._api.delete(f'folders/{self.oid}')
