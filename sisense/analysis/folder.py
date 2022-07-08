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

    def update(self, **kwargs):
        """
        Update the current folder.

        :param name: (str, named parameter) The new folder name.
        :param parentId: (str, named parameter) The new parent folder ID.
        :param owner: (str, named parameter) The new owner of the folder, a user ID.
        """
        data = {
            'name': kwargs.get('name', self.name),
            'parentId': kwargs.get('parentId', self.parentId),
            'owner': kwargs.get('owner', self.owner)
        }

        self._api.patch(f'folders/{self.oid}', data=data)

    def delete(self):
        """Delete the current folder."""
        self._api.delete(f'folders/{self.oid}')
