from sisense.resource import Resource
import json


class Datasource(Resource):

    def to_csv(self, datasource, metadata: list) -> str:
        """
        Execute JAQL and return the result as CSV.

        :param datasource: (str or dict) Elasticube name or datasource representation as JSON.
        :param metadata: (list) A list of JAQL representations as dict. See https://sisense.dev/reference/jaql/ for details.
        :return: (pandas.DataFrame) Data as CSV represent by a pandas.DataFrame.
        """
        data = [('data', json.dumps({'datasource': datasource, 'metadata': metadata}))]
        headers = {'Accept': '*/*'}

        response = self._api.post('datasources/x/jaql/csv', data=data, headers=headers)

        data = response['message']
        return data

    def from_sql(self, datasource, query: str) -> dict:
        """
        Execute a SQL statement in the specified datasource.

        :param datasource: (str or dict) Elasticube name or datasource representation as JSON.
        :param query: (str) A SQL statement.
        :return: (dict) {"headers": list, "values": list of lists}
        """
        datasource_title = datasource['title'] if type(datasource) is dict else datasource
        response = self._api.get(f'datasources/{datasource_title}/sql', query={'query': query})
        return response
