from .test_case import TestCaseV1 as TestCase
from sisense.admin import Group


class GroupTestCase(TestCase):

    def test_get(self):
        group = self.sisense.group.get(self.config['group_name'])
        self.assertEqual(group.name, self.config['group_name'])

        same = self.sisense.group.get(oid=group._id)
        self.assertEqual(group._id, same._id)
        self.assertEqual(group.name, same.name)

    def create(self):
        group = self.sisense.group.create(self.config['group_name'])

        self.assertIsInstance(group, Group)
        self.assertEqual(group.name, self.config['group_name'])

    def delete(self):
        group = self.sisense.group.get(self.config['group_name'])
        if group:
            group.delete()

            group = self.sisense.group.get(self.config['group_name'])
            self.assertEqual(group, None)
