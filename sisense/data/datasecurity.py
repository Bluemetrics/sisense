from sisense.resource import Resource
from sisense.api import API


class DataSecurity(Resource):

    def __init__(self, api: API, rjson: dict = None, elasticube_name: str = None):
        super().__init__(api, rjson)
        self._elasticube = elasticube_name

    def all(self, table: str = None, column: str = None, elasticube: str = None) -> list:
        """
        Get elasticube's data security rules. If 'table' and 'column' are specified, get rules for that specific column.

        :param table: (str, default None) Datatable's name.
        :param column: (str, default None) Column's name.
        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.
        :return: (list) of DataSecurity objects
        """
        elasticube = elasticube if elasticube else self._elasticube
        tbl_col = f'/{table}/{column}' if table and column else ''

        content = self._api.get(f'elasticubes/localhost/{elasticube}/datasecurity{tbl_col}')

        results = [DataSecurity(self._api, rjson, elasticube) for rjson in content]
        return results

    def get(self, oid: str, elasticube: str = None) -> Resource:
        """
        Get the specified data security rule.

        :param oid: (str) Rule's ID.
        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.
        :return: (DataSecurity) if found. Otherwise, None.
        """
        for rule in self.all(elasticube=elasticube):
            if rule._id == oid:
                return rule

        return None

    def create(self, table: str, column: str, datatype: str, shares: list, elasticube: str = None, **kwargs) -> Resource:
        """
        Create a new data security rule.

        :param table: (str) Datatable's name.
        :param column: (str) Column's name.
        :param datatype: (str) Type of data. For example: 'text'.
        :param shares: (list) List of shares dict {'party': <user/group id>, 'type': <'user' or 'group'>}
        :param members: (list, default None) Values considered. For example: if column is CountryName, then members can be a list of country names to allow or deny.
        :param all_members: (bool, default True) Whether to apply the rules for all members. If members is set, this parameter is ignored.
        :param exclusionary: (bool, default True) Allow (False) or deny (True) members.
        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.
        :return: (DataSecurity) The new data security rule.
        """
        elasticube = elasticube if elasticube else self._elasticube
        data = self._payload(table, column, datatype, shares, **kwargs)

        content = self._api.post(f'elasticubes/localhost/{elasticube}/datasecurity', data=[data])
        result = DataSecurity(self._api, content[0], elasticube)

        return result

    def update(self) -> Resource:
        """Update the current data security rule.

        :return: (DataSecurity) updated.
        """
        self.fix_shares()
        data = self._payload(**self.json)

        content = self._api.put(f'elasticubes/datasecurity/{self._id}', data=data)

        return DataSecurity(self._api, content, self._elasticube)

    def delete(self):
        """Delete the current data security rule."""
        self._api.delete(f'elasticubes/datasecurity/{self._id}')

    def delete_all(self, table: str = None, column: str = None, elasticube: str = None):
        """
        Delete data security rules for a specific column.

        :param table: (str, default None) Datatable's name. If None, use self.table.
        :param column: (str, default None) Column's name. If None, use self.column.
        :param elasticube: (str, default None) Elasticube's name. If None, use self.elasticube.
        """
        elasticube = elasticube if elasticube else self._elasticube
        table = table if table else self.table
        column = column if column else self.column

        self._api.delete(f'elasticubes/localhost/{elasticube}/datasecurity', query={'table': table, 'column': column})

    def _payload(self,
                 table: str,
                 column: str,
                 datatype: str,
                 shares: list,
                 **kwargs):
        data = {
            'table': table,
            'column': column,
            'datatype': datatype,
            'shares': shares,
        }

        if 'exclusionary' in kwargs:
            data['exclusionary'] = kwargs['exclusionary']

        if 'members' in kwargs:
            data['members'] = kwargs['members']
            data['allMembers'] = None
        else:
            data['allMembers'] = kwargs['all_members']
            data['members'] = []

        return data
