from sisense.resource import Resource
from time import time


class Grafana(Resource):

    def query(self, expression: str, start: int = None, end: int = None, step: int = 30) -> dict:
        """
        Execute a query in Grafana.

        :param expression: (str) A Grafana's expression.
        :param start: (int, default None) Timestamp in seconds. If start is None, start = time.now().
        :param end: (int, default None) Timestamp in seconds. If end is None, end = start.
        :param step: (int, default 30) Sample the data every "step" seconds.
        :return: (dict) The Grafana's result. Example:
            {
                "status": "success",
                "data": {
                    "resultType": "matrix",
                    "result": [  # one for each node
                        {
                            "metric": {
                                "container": <str>,
                                "endpoint": <str>,
                                "instance": <str>,
                                "job": <str>,
                                "namespace": <str>,
                                "pod": <str>,
                                "service": <str>
                            },
                            "values": [
                                [<timestamp>, <str (expected value)>],
                                ...
                            ]
                        },
                        ...
                    ]
                }
            }
        """
        if not start:
            start = int(time())

        if not end:
            end = start

        params = {
            'query': expression,
            'start': start,
            'end': end,
            'step': step
        }

        content = self._api.get('grafana/api/datasources/proxy/1/api/v1/query_range', query=params)
        return content
