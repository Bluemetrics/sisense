from .test_case import TestCaseV1 as TestCase
from sisense.admin import User


class UserTestCase(TestCase):

    def test_get(self):
        user = self.sisense.user.get(self.config['user_email'])
        self.assertEqual(user.email, self.config['user_email'])

        same = self.sisense.user.get(oid=user._id)
        self.assertEqual(user._id, same._id)
        self.assertEqual(user.email, same.email)

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
