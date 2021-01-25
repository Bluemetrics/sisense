from sisense.resource import Resource


class Elasticube(Resource):

    def all(self) -> list:
        """
        Get all elasticubes.

        :return: (list) of Elasticube objects.
        """
        content = self._api.get('elasticubes/getElasticubes')
        return [Elasticube(self._api, rjson) for rjson in content]
