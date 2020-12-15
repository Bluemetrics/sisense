from sisense.resource import Resource
from sisense.api import API


class Hierarchy(Resource):

    def __init__(self, api: API, rjson: dict = None, elasticube_name: str = None):
        super().__init__(api, rjson)
        self._elasticube = elasticube_name

    def all(self, elasticube: str = None) -> list:
        """
        Get elasticube's hierarchies.

        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.
        :return: a list of Hierarchy objects
        """
        elasticube = elasticube if elasticube else self._elasticube
        query = {'elasticube': elasticube, 'server': 'localhost'}

        content = self._api.get(f'elasticubes/hierarchies', query=query)
        hierarchies = [Hierarchy(self._api, h, elasticube) for h in content]

        return hierarchies

    def get(self, oid: str, elasticube: str = None) -> Resource:
        """
        Get the specified hierarchy.

        :param oid: (str) Hierarchy's ID.
        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.
        :return: (Hierarchy) if found. Otherwise, None.
        """
        for hierarchy in self.all(elasticube):
            if hierarchy._id == oid:
                return hierarchy

        return None

    def create(self, title: str, levels: list, always_included: bool, elasticube: str = None) -> Resource:
        """
        Create a new hierarchy.

        :param title: (str) Hierarchy's title.
        :param levels: (list) List of dict {'title': str, 'table': str, 'column': str, 'datatype': str, 'dim': str, index: int}.
        :param always_included: (bool) Whether to always include the hierarchy on widget.
        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.
        :return: (Hierarchy) The new hierarchy.
        """
        elasticube = elasticube if elasticube else self._elasticube
        data = {'title': title, 'levels': levels, 'alwaysIncluded': always_included}

        content = self._api.post(f'elasticubes/localhost/{elasticube}/hierarchies', data=data)
        return Hierarchy(self._api, content, elasticube)

    def delete(self):
        """Delete the current hierarchy."""
        self._api.delete(f'elasticubes/localhost/{self._elasticube}/hierarchies/{self._id}')
