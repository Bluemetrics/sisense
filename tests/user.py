from .test_case import TestCaseV1 as TestCase


class UserTestCase(TestCase):

    def test_get(self):
        user = self.sisense.user.get(self.config['user_email'])
        self.assertEqual(user.email, self.config['user_email'])

        same = self.sisense.user.get(oid=user._id)
        self.assertEqual(user._id, same._id)
        self.assertEqual(user.email, same.email)
