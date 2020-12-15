from sisense.resource import Resource


class Build(Resource):

    PENDING = 'pending'
    BUILDING = 'building'
    DONE = 'done'
    CANCELLED = 'cancelled'
    FAILED = 'failed'

    def is_initialized(self) -> bool:
        """
        True, if build has a status.

        :return: (bool)
        """
        return self.status is not None

    def is_pending(self) -> bool:
        """
        True, if build has pending status.

        :return: (bool)
        """
        return self.status == self.PENDING

    def is_building(self) -> bool:
        """
        True, if build has building status.

        :return: (bool)
        """
        return self.status == self.BUILDING

    def is_done(self) -> bool:
        """
        True, if build is done.

        :return: (bool)
        """
        return self.status == self.DONE

    def was_cancelled(self) -> bool:
        """
        True, if build was cancelled.

        :return: (bool)
        """
        return self.status == self.CANCELLED

    def has_failed(self) -> bool:
        """
        True, if build has failed.

        :return: (bool)
        """
        return self.status == self.FAILED

    def is_finished(self) -> bool:
        """
        True, if build is not running nor pending.

        :return: (bool)
        """
        return self.is_done() or self.was_cancelled() or self.has_failed()

    def get(self, oid: str) -> Resource:
        """
        Get a build task by id.

        :param oid: (str) Build ID.

        :return: Build
        """
        content = self._api.get(f'builds/{oid}')
        return Build(self._api, content)

    def update(self):
        """Update this build information."""
        self.json = self.get(self.oid).json

    def all(self, datamodel_id: str = None, status: str = None) -> list:
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

    def start(self, datamodel_id: str, build_type: str = 'schema_changes', row_limit: int = None) -> Resource:
        """
        Start a new build.

        :param datamodel_id: (str) Datamodel ID.
        :param build_type: (str, default 'schema_changes') Type of build. Possible values: schema_changes, by_table, full
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
        self.update()
