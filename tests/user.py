from .test_case import TestCaseV1 as TestCase
from sisense.admin import User


class UserTestCase(TestCase):

    def test_get(self):
        user = self.sisense.user.get(self.config['user_email'])
        self.assertEqual(user.email, self.config['user_email'])

        same = self.sisense.user.get(oid=user._id)
        self.assertEqual(user._id, same._id)
        self.assertEqual(user.email, same.email)

    def test_all(self):
        user = self.sisense.user.get(self.config['user_email'])
        users = self.sisense.user.all(email=self.config['user_email'])

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, user.email)
        self.assertEqual(users[0]._id, user._id)

        users = self.sisense.user.all()
        self.assertGreater(len(users), 1)

        for u in users:
            self.assertIsInstance(u, User)

    def test_update(self):
        user = self.sisense.user.get(self.config['user_email'])
        user.update(firstName='Dev', lastName='Team')

        user = self.sisense.user.get(self.config['user_email'])
        self.assertEqual(user.firstName, 'Dev')
        self.assertEqual(user.lastName, 'Team')

    def create(self):
        name = 'DevTeam'
        user = self.sisense.user.create(self.config['user_email'], userName=name, firstName=name + ' (1)')

        self.assertIsInstance(user, User)
        self.assertEqual(user.userName, name)
        self.assertEqual(user.firstName, name + ' (1)')

    def delete(self):
        user = self.sisense.user.get(self.config['user_email'])
        if user:
            user.delete()

            user = self.sisense.user.get(self.config['user_email'])
            self.assertEqual(user, None)
