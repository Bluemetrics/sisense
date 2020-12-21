from sisense.resource import Resource


class Dashboard(Resource):

    def get(self, oid: str = None, name: str = None, folder: str = None) -> Resource:
        """
        Get the specified dashboard. At least, one of the parameters must be set.
        If found more than one dashboard with the same name, the first one is returned.

        :param oid: (str, default None) Dashboard's ID.
        :param name: (str, default None) Dashboard's name.
        :param folder: (str, default None) Parent folder's ID. Used when 'name' is set.
        :return: (Dashboard) Dashboard, if found. None, otherwise.
        """
        if not oid and not name:
            raise ValueError('At least, one of the parameters must be set. Both oid and name are None.')

        if oid:
            content = self._api.get(f'dashboards/{oid}')
        else:
            content = self._api.get('dashboards', query={'name': name, 'parentFolder': folder})
            content = content[0] if len(content) else None

        if not content:
            return None

        result = Dashboard(self._api, content)
        return result

    def get_shares(self) -> list:
        """Get shares for the current dashboard."""
        content = self._api.get(f'dashboards/{self.oid}/shares')
        return content

    def update(self, **kwargs):
        """
        Update the current dashboard information according to the specified parameters.
        For more information, check "PATCH /dashboards/{id}" on https://sisense.dev/reference/rest/v1.html.
        """
        data = kwargs
        data['oid'] = self.oid

        content = self._api.patch(f'dashboards/{self.oid}', data=data)
        self.json = content

    def exists(self, oid: str = None) -> bool:
        """
        Check whether a specific dashboard exists.

        :param oid: (str, default self.oid) Dashboard's ID.
        :return: (bool) True, if dashboard exists.
        """
        oid = oid if oid else self.oid
        content = self._api.get(f'dashboards/{oid}/exists')
        return content['exists']

    def do_import(self, action: str = 'duplicate') -> Resource:
        """
        Import the current dashboard.

        :param action: (str, default 'duplicate') Determines if the existing dashboard should be overwritten. Possible values : skip, overwrite, duplicate.
        :return: (Dashboard) The new dashboard.
        """
        query = {'action': action, 'importFolder': self.parentFolder}

        content = self._api.post('dashboards/import/bulk', query=query, data=[self.json])
        return Dashboard(self._api, content['succeded'][0])

    def publish(self):
        """Publish the current dashboard."""
        self._api.post(f'dashboards/{self.oid}/publish', query={'force': True})

    def delete(self):
        """Delete the current dashboard."""
        self._api.delete(f'dashboards/{self.oid}')
