from sisense.resource import Resource


class Connection(Resource):

    def all(self, **kwargs) -> list:
        """
        Get all connections.

        :param kwargs: Optional keyword arguments.
            - sort: (str) Field by which the result should be sorted.
            - skip: (int) Number the results to skip from the start. USe for paging.
            - limit: (int) Nuber of results to retrieve.
        :return: a list of Connection objects.
        """
        content = self._api.get('connection', query=kwargs)
        connections = [Connection(self._api, c) for c in content]

        return connections

    def get(self, oid: str) -> Resource:
        """
        Get the specified connection.

        :param oid: (str) Connections's ID.
        :return: (Connection)
        """
        content = self._api.get(f'connection/{oid}')
        return Connection(self._api, content)

    def create(self, **kwargs) -> Resource:
        """
        Create a new connection.

        :param kwargs: Keyword arguments.
            - owner: (str) User's ID.
            - provider: (str) Connection type: Excel, MySQL, MS SQL...
            - timeout: (int) Connection timeout.
            - refreshRate: (float) Optional. Just for live models.
            - timezone: (str) Optional. Timezone.
            - schema: (str) Database schema that will be used.
            - parameters: (dict) Other parameters such as UserName, Password, Database...
        :return: (Connection) The new connection.
        """
        content = self._api.post('connection', data=kwargs)
        return Connection(self._api, content)

    def update(self, **kwargs) -> Resource:
        """
        Update the current connection.

        :param kwargs: Keyword arguments.
            - owner: (str) User's ID.
            - provider: (str) Connection type: Excel, MySQL, MS SQL...
            - timeout: (int) Connection timeout.
            - refreshRate: (float) Optional. Just for live models.
            - timezone: (str) Optional. Timezone.
            - schema: (str) Database schema that will be used.
            - parameters: (dict) Other parameters such as UserName, Password, Database...
        :return: (Connection) The updated connection.
        """
        content = self._api.patch(f'connection/{self._id}', data=kwargs)
        return Connection(self._api, content)

    def delete(self):
        """Delete the current connection."""
        self._api.delete(f'connection/{self._id}')
