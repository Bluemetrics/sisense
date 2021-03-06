from sisense.resource import Resource


class Elasticube(Resource):

    def all(self) -> list:
        """
        Get all elasticubes.

        :return: (list) of Elasticube objects.
        """
        content = self._api.get('elasticubes/getElasticubes')
        return [Elasticube(self._api, rjson) for rjson in content]

    def get(self, name: str) -> Resource:
        """
        Get elasticube.

        :param name: (str) Elasticube's name.
        :return: (Elasticube)
        """
        content = self._api.get(f'elasticubes/servers/next/localhost/{name}')
        return Elasticube(self._api, content)
