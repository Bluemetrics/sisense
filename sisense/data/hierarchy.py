from sisense.resource import Resource
from sisense.api import API


class Hierarchy(Resource):

    def __init__(self, api: API, rjson: dict = None, elasticube: str = None):
        super().__init__(api, rjson)
        self._elasticube = elasticube

    def get(self, elasticube: str) -> list:
        """Get elasticube's hierarchies.

        :param elasticube: (str) Elasticube's name.
        :return: a list of Hierarchy objects
        """
        query = {'elasticube': elasticube, 'server': 'localhost'}
        content = self._api.get(f'elasticubes/hierarchies', query=query)

        hierarchies = [Hierarchy(self._api, h, elasticube) for h in content]
        return hierarchies

    def add(self, elasticube: str = None, hierarchy: object = None) -> object:
        """Add a new hierarchy

        :param elasticube: (str, default None) Elasticube's name.
        :param hierarchy: (Hierarchy, default None) If None, add self.
        :return: (Hierarchy)
        """
        elasticube = elasticube if elasticube else self._elasticube
        hierarchy = hierarchy if hierarchy else self
        always_included = hierarchy.alwaysIncluded if hasattr(hierarchy, 'alwaysIncluded') else False

        data = {'title': hierarchy.title, 'levels': hierarchy.levels, 'alwaysIncluded': always_included}
        content = self._api.post(f'elasticubes/localhost/{elasticube}/hierarchies', data=data)

        return Hierarchy(self._api, content)

    def delete(self):
        """Delete the current hierarchy."""
        self._api.delete(f'elasticubes/localhost/{self._elasticube}/hierarchies/{self._id}')
