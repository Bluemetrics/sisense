from sisense.resource import Resource


class Build(Resource):

    def get(self, oid: str) -> Resource:
        """
        Get a build task by id.

        :param oid: (str) Build ID.

        :return: Build
        """
        content = self._api.get(f'builds/{oid}')
        return Build(self._api, content['builds'][0])

    def tasks(self, datamodel_id: str = None, status: str = None) -> list:
        """
        Get a list of build tasks.

        :param datamodel_id: (str, default None) ID of Datamodel to filter results by.
        :param status: (str, default None) Build status to filter results by. Possible values: pending, building, done, failed, cancelled.

        :return: (list) List of Build objects.
        """
        query = {}
        if datamodel_id:
            query['datamodelId'] = datamodel_id

        if status:
            query['status'] = status

        content = self._api.get('builds', query=query)
        return [Build(self._api, task) for task in content]

    def start(self, datamodel_id: str, build_type: str = 'schema_changes', row_limit: int = 0) -> Resource:
        """
        Start a new build.

        :param datamodel_id: (str) Datamodel ID.
        :param build_type: (str, default 'schema_changes') Type of build. Possible values: schema_changes, replace_all
        :param row_limit: (int) Row limit.

        :return: Build
        """
        data = {'datamodelId': datamodel_id,
                'buildType': build_type,
                'rowLimit': row_limit}

        content = self._api.post('builds', data=data)
        return Build(self._api, content)

    def stop(self):
        """Cancel/stop this build."""
        self._api.delete(f'builds/{self.oid}')

    def stop_all(self, datamodel_id: str):
        """
        Cancel/stop all running build tasks for a specific Datamodel.

        :param datamodel_id: (str) Datamodel ID.
        """
        query = {'datamodelId': datamodel_id}
        self._api.delete('builds', query=query)

