from sisense.resource import Resource
from .build import Build
import json


class Datamodel(Resource):

    def get(self, oid: str = None, title: str = None) -> Resource:
        """
        Get datamodel by ID. At least one of the parameters should be set.

        :param oid: (str, default None) Datamodel's ID to search for.
        :param title: (str, default None) Datamodel's title to search for. If oid is set, title is ignored.

        :return: Datamodel
        """
        if not oid and not title:
            raise ValueError('At least one parameter should be set.')

        if oid:
            content = self._api.get(f'datamodels/{oid}/schema')
        else:
            query = {'title': title, 'limit': 1}
            content = self._api.get('datamodels/schema', query=query)
            content = content[0]

        return Datamodel(self._api, content)

    def get_builds(self, status: str = None) -> list:
        """
        Get a list of build tasks for this datamodel.

        :param status: (str, default None) Build status to filter results by. Possible values: pending, building, done, failed, cancelled.

        :return: (list) List of Build objects.
        """
        return Build(self._api).tasks(self.oid, status)

    def create(self, title: str, server: str = 'LocalHost', ctype: str = 'extract') -> Resource:
        """
        Create a new datamodel.

        :param title: (str) Datamodel's title.
        :param server: (str, default 'LocalHost') Server in which the datamodel should be created.
        :param ctype: (str, default 'extract') Creation type.

        :return: (Datamodel) The new datamodel.
        """
        data = {'title': title, 'server': server, 'type': ctype}
        content = self._api.post('datamodels', data=data)
        return Datamodel(self._api, content)

    def clone(self, title: str) -> Resource:
        """
        Clone this datamodel.

        :param title: (str) Datamodel's title.

        :return: (Datamodel) The new datamodel.
        """
        data = {'title': title}
        content = self._api.post(f'datamodels/{self.oid}/clones', data=data)
        return Datamodel(self._api, content)

    def delete(self):
        """Delete this data model."""
        self._api.delete(f'datamodels/{self.oid}')

    def export_datamodel(self, filepath: str, full: bool = False):
        """
        Export the datamodel.

        :param filepath: (str) Where to save the downloaded file, including file's name.
        :param full: (bool, default False) If true, export datamodel with schema and data. Otherwise, only export datamodel's schema.
        """
        self._download_full(filepath) if full else self._download_schema(filepath)

    def import_datamodel(self, title: str, filepath: str, full: bool = False) -> Resource:
        """
        Import a datamodel.

        :param title: (str) New datamodel's title.
        :param filepath: (str) Where to get data for import, including file's name.
        :param full: (bool, default False) If true, import datamodel with schema and data. Otherwise, only import datamodel's schema.

        :return: (Datamodel) The new datamodel.
        """
        self._upload_full(title, filepath) if full else self._upload_schema(title, filepath)
        return self.get(title=title)

    def start_build(self, build_type: str = 'schema_changes', row_limit: int = 0) -> Resource:
        """
        Start a build task for this datamodel.

        :param build_type: (str, default 'schema_changes') Type of build. Possible values: schema_changes, replace_all
        :param row_limit: (int) Row limit.

        :return: (Build) Build task created.
        """
        return Build(self._api).start(self.oid, build_type, row_limit)

    def stop_builds(self):
        """Cancel/stop all running build tasks for this Datamodel."""
        Build(self._api).stop_all(self.oid)

    def _download_schema(self, filepath: str):
        query = {'datamodelId': self.oid, 'type': 'schema-latest'}
        content = self._api.get('datamodel-exports/schema', query=query)

        with open(filepath, 'w') as file:
            json.dump(content, file)

    def _download_full(self, filepath):
        query = {'datamodelId': self.oid}
        self._api.download('datamodel-exports/stream/full', filepath, query=query)

    def _upload_schema(self, title: str, filepath: str):
        with open(filepath, 'r') as file:
            schema = json.load(file)

        schema['title'] = title
        query = {'newTitle': title}
        data = {'Body': schema}

        self._api.post('datamodel-imports/schema', data=data, query=query)

    def _upload_full(self, title: str, filepath: str):
        query = {'newTitle': title}

        with open(filepath, 'rb') as file:
            self._api.upload('datamodel-imports/stream/full', file=file, query=query)

