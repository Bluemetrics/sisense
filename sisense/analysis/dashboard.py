from sisense.resource import Resource
import json


class Dashboard(Resource):

    def all(self, **kwargs) -> list:
        """
        Get all dashboards.

        :param kwargs: Keywords optional arguments.
            - parentFolder: (str) Folder ID.
            - name: (str) Dashboard's name.
            - datasourceTitle: (str) Elasticube title used as datasource.
            - datasourceAddress: (str) Elasticube address.
            - fields: (list) List of fields to retrieve for each dashboard.
            - expand: (list) List of fields to be expanded (convert IDs to the actual object).
        :return: (list) List of Dashboard objects.
        """
        content = self._api.get('dashboards', query=kwargs)
        dashboards = [Dashboard(self._api, rjson) for rjson in content]
        return dashboards

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

    def do_import(self, filepath: str, action: str = 'duplicate', folder: str = None) -> Resource:
        """
        Import dashboard from file in filepath.

        :param filepath: (str) Relative/absolute path to a .dash file.
        :param action: (str, default 'duplicate') Determines if the existing dashboard should be overwritten. Possible values : skip, overwrite, duplicate.
        :param folder: (str, default None) Folder's ID where the dashboard should be imported.
        :return: (Dashboard) The new dashboard.
        """
        with open(filepath, 'r') as file:
            rjson = json.load(file)

        query = {'action': action, 'importFolder': folder}
        content = self._api.post('dashboards/import/bulk', query=query, data=[rjson])

        return Dashboard(self._api, content['succeded'][0])

    def do_export(self, filepath: str, filetype: str = 'dash', **kwargs):
        """
        Export the current dashboard.

        :param filepath: (str) Where to save the file including file's name and extension.
        :param filetype: (str, default 'dash') Type of export. Possible values: dash, png, pdf.

        For more details on other parameters, check:
        <GET /dashboards/{id}/export/*> on https://sisense.dev/reference/rest/v1.html.
        """
        content = self._api.get(f'dashboards/{self.oid}/export/{filetype}', query=kwargs)
        dashboard = Dashboard(self._api, content)
        dashboard.save(filepath)

    def publish(self):
        """Publish the current dashboard."""
        self._api.post(f'dashboards/{self.oid}/publish')

    def delete(self):
        """Delete the current dashboard."""
        self._api.delete(f'dashboards/{self.oid}')
