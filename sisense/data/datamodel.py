from sisense.resource import Resource
from sisense.cli import CLI
from sisense.api import API
import json


class Datamodel(Resource):

    def __init__(self, api: API, rjson: dict = None):
        """
        Super for any API's resource.

        :param api: (API) Used to make API's requests.
        :param rjson: (dict) Resource representation.
        """
        super(Datamodel, self).__init__(api, rjson)
        self._cli = CLI(api)

    def list(self):
        """
        Get the following information for each elasticube:
            - instance: Query instance
            - id: elasticube's ID
            - name: elasticube's name
            - runtime_status: RUNNING or STOPPED
            - index_size: LONG or SHORT
            - path: path to the elasticube data on Linux
            - shadow_path: (?)
            - next_path: in case the elasticube is divided into two paths
            - last_failure_message: if build failed, shows the last message

        :return: (list) a list of Datamodel objects
        """
        response = self._cli.execute('elasticubes list')

        lines = response['message'].split('\n')
        keys = [key.strip().lower().replace(' ', '_') for key in lines[1].split('|')][1:-1]

        result = []
        for line in lines[3:-1]:
            values = [value.strip() if len(value.strip()) else None for value in line.split('|')][1:-1]
            rjson = dict(zip(keys, values))
            datamodel = Datamodel(self._api, rjson)
            result.append(datamodel)

        return result

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

        return Datamodel(self._api, content)

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

    def start(self):
        """Start this data model."""
        name = self.name if 'name' in self.json else self.title
        self._cli.execute(f'elasticubes start -name "{name}"')

    def stop(self):
        """Stop this data model."""
        name = self.name if 'name' in self.json else self.title
        self._cli.execute(f'elasticubes stop -name "{name}"')

    def do_export(self, filepath: str, full: bool = False):
        """
        Export the datamodel.

        :param filepath: (str) Where to save the downloaded file, including file's name.
        :param full: (bool, default False) If true, export datamodel with schema and data. Otherwise, only export datamodel's schema.
        """
        self._download_full(filepath) if full else self._download_schema(filepath)

    def do_import(self, title: str, filepath: str, full: bool = False) -> Resource:
        """
        Import a datamodel.

        :param title: (str) New datamodel's title.
        :param filepath: (str) Where to get data for import, including file's name.
        :param full: (bool, default False) If true, import datamodel with schema and data. Otherwise, only import datamodel's schema.

        :return: (Datamodel) The new datamodel.
        """
        self._upload_full(title, filepath) if full else self._upload_schema(title, filepath)
        return self.get(title=title)

    def get_latest_build_log(self, start_from: int = 1):
        """
        Get datamodel's latest build log.

        :param start_from: (int, default 1) From log sequence number.
        :return: (list) Logs. Example:
            [{
                "timestamp": "2022-10-25T19:03:12.069Z",
                "verbosity": "Info",
                "type": "buildFlow",
                "message": "Waiting in queue",
                "trackId": "77d24bba-c7f8-4c47-9de9-a64bc5a7e746",
                "contextRef": null,
                "serverId": "7c3f73dd-0b38-48dc-9347-c78811bd80c4",
                "serverName": "localhost",
                "cubeId": "Bot",
                "sessionId": "0c2152c0-d716-4579-895e-1f24f3aa8670",
                "buildSeq": 1,
                "typeValue": {
                    "tableName": null,
                    "columnName": null,
                    "trackingItemEventId": null,
                    "title": "Waiting in queue",
                    "description": "Waiting in queue",
                    "additionalInfo": null,
                    "__typename": "BuildLogGeneralInfoTypeValue"
                },
                "serverTime": "2022-10-28T17:42:00.795Z",
                "__typename": "BuildLogEntry"
            }, ...]
        """
        data = {
            'query': "query ($elasticubeOid: UUID!, $fromSequenceNumber: Int) {  getRecentBuildLogs(elasticubeOid: $elasticubeOid, fromSequenceNumber: $fromSequenceNumber) {    ...buildLogsData    __typename  }}fragment buildLogsData on BuildLogEntry {  timestamp  verbosity  type  message  trackId  contextRef  serverId  serverName  cubeId  sessionId  buildSeq  typeValue {    tableName    columnName    ... on BuildLogGeneralFailureTypeValue {      trackingItemEventId      title      description      additionalInfo      message      source      __typename    }    ... on BuildLogGeneralInfoTypeValue {      trackingItemEventId      title      description      additionalInfo      __typename    }    ... on BuildLogIndexingTypeValue {      dateTimeNowInTicks      chunkSize      totalToIndex      currentIndexed      completionState      startTime      endTime      cloudName      traceLevel      __typename    }    ... on BuildLogChunkTypeValue {      trackingItemEventId      title      description      additionalInfo      countRecords      totalRecords      chunkID      __typename    }    ... on BuildLogSqlBasedTypeValue {      trackingItemEventId      title      description      additionalInfo      sql      __typename    }    ... on BuildLogStartEndTypeValue {      trackingItemEventId      title      description      additionalInfo      physicalSize      __typename    }    ... on BuildLogBuildFlowTypeValue {      dependencies {        sortedDependencies {          name          type          table          dependencies          __typename        }        __typename      }      __typename    }    __typename  }  serverTime  __typename}",
            'variables': {'elasticubeOid': self.oid, 'fromSequenceNumber': start_from},
            'operationName': None
        }

        content = self._api.post('ecm', data=data)
        return content['data']['getRecentBuildLogs']

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

        query = {'newTitle': title}
        self._api.post('datamodel-imports/schema', data=schema, query=query)

    def _upload_full(self, title: str, filepath: str):
        query = {'newTitle': title}
        data = {'fileToUpload': open(filepath, 'rb')}
        self._api.upload('datamodel-imports/stream/full', file=data, query=query)


