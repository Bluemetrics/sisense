from sisense.resource import Resource


class DataSecurity(Resource):

    def get(self, elasticube: str) -> list:
        """Get elasticube's data security rules.

        :param elasticube: (str) Elasticube's name.
        :return: a list of DataSecurity objects
        """
        content = self._api.get(f'elasticubes/localhost/{elasticube}/datasecurity')
        results = [DataSecurity(self._api, rjson) for rjson in content]

        return results

    def add(self, elasticube: str, datasecurity: object = None) -> object:
        """Add a new data security rule.

        :param elasticube: (str) Elasticube's name.
        :param datasecurity: (DataSecurity, default None) If None, add self.
        :return: (DataSecurity)
        """
        elasticube = elasticube if elasticube else self.elasticube
        datasecurity = datasecurity if datasecurity else self
        data = self._data(datasecurity)

        content = self._api.post(f'elasticubes/localhost/{elasticube}/datasecurity', data=[data])
        result = DataSecurity(self._api, content[0])

        return result

    def update(self, datasecurity: object) -> object:
        """Update the current data security rule.

        :param datasecurity: (DataSecurity) Data security object with new configuration.
        :return: (DataSecurity) updated.
        """
        data = self._data(datasecurity)
        content = self._api.put(f'elasticubes/datasecurity/{self._id}', data=data)

        return DataSecurity(self._api, content)

    def delete(self):
        """Delete the current data security rule."""
        self._api.delete(f'elasticubes/datasecurity/{self._id}')

    def _data(self, datasecurity: object) -> dict:
        shares = datasecurity.shares
        for i, share in enumerate(shares):
            if 'partyId' in share:
                share['party'] = share['partyId']

            share.pop('partyId', None)
            share.pop('partyName', None)

            shares[i] = share

        data = {
            'column': datasecurity.column,
            'shares': shares,
            'table': datasecurity.table,
            'datatype': datasecurity.datatype
        }

        if hasattr(datasecurity, 'exclusionary'):
            data['exclusionary'] = datasecurity.exclusionary

        if hasattr(datasecurity, 'allMembers') and datasecurity.allMembers:
            data['allMembers'] = datasecurity.allMembers
        else:
            data['members'] = datasecurity.members

        return data
