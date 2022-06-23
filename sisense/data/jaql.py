from sisense.resource import Resource
import pandas as pd
import json
import io


class JAQL(Resource):

    def to_csv(self, datasource, metadata: list) -> pd.DataFrame:
        """
        Execute JAQL and return the result as CSV.

        :param datasource: (str or dict) Elasticube name or datasource representation as JSON.
        :param metadata: (list) A list of JAQL representations as dict. See https://sisense.dev/reference/jaql/ for details.
        :return: (pandas.DataFrame) Data as CSV represent by a pandas.DataFrame.
        """
        data = [('data', json.dumps({'datasource': datasource, 'metadata': metadata}))]
        headers = {'Accept': '*/*'}

        response = self._api.post('datasources/x/jaql/csv', data=data, headers=headers)

        data = io.StringIO(response['message'])
        dataframe = pd.read_csv(data, header=0, index_col=None)

        return dataframe
