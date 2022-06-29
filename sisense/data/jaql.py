from sisense.resource import Resource
import json


class JAQL(Resource):

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
