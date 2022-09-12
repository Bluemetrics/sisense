from sisense.resource import Resource
import json


class Widget(Resource):

    def to_pdf(self, filepath: str, **kwargs):
        """
        Export the current widget to PDF and save it on filepath.

        :param filepath: (str) Path to save the file in, including filename and extension.
        :param kwargs: (named parameters) Example:
            {
                'paperFormat': 'A4',
                'paperOrientation': 'landscape',
                'showTitle': False,
                'showFooter': True,  # to show page number
                'title': 'Title',
                'rowCount': 8000
            }
        """
        params = {
            'paperFormat': 'A4',
            'paperOrientation': 'portrait',
            'showTitle': False,
            'showFooter': True,
            'title': 'Title',
            'rowCount': 8000
        }

        params.update(kwargs)
        response = self._api.post(f'export/dashboards/{self.dashboardid}/widgets/{self.oid}/pdf',
                                  headers={'Accept': 'application/pdf'},
                                  data={'params': params})

        with open(filepath, 'wb') as file:
            file.write(response['message'])

    def update(self):
        raise NotImplementedError
