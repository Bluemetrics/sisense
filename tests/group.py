from .test_case import TestCaseV1 as TestCase
from sisense.admin import Group


class GroupTestCase(TestCase):

    def test_get(self):
        group = self.sisense.group.get(self.config['group_name'])
        self.assertEqual(group.name, self.config['group_name'])

        same = self.sisense.group.get(oid=group._id)
        self.assertEqual(group._id, same._id)
        self.assertEqual(group.name, same.name)

    def test_all(self):
        group = self.sisense.group.get(self.config['group_name'])
        groups = self.sisense.group.all(name=self.config['group_name'])

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].name, group.name)
        self.assertEqual(groups[0]._id, group._id)

        groups = self.sisense.group.all()
        self.assertGreater(len(groups), 1)

        for g in groups:
            self.assertIsInstance(g, Group)

    def test_add_user(self):
        group = self.sisense.group.get(self.config['group_name'])
        user = self.sisense.user.create(self.config['user_email'])

        group.add_user(user)
        user = self.sisense.user.get(self.config['user_email'])

        user.delete()
        self.assertEqual(user.groups[0], group._id)

    def test_remove_user(self):
        group = self.sisense.group.get(self.config['group_name'])
        user = self.sisense.user.create(self.config['user_email'])

        group.add_user(user)
        user = self.sisense.user.get(self.config['user_email'])
        self.assertEqual(user.groups[0], group._id)

        group.remove_user(user)

        user = self.sisense.user.get(self.config['user_email'])
        user.delete()

        self.assertEqual(len(user.groups), 0)

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
