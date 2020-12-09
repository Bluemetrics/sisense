from .test_case import TestCaseV09 as TestCase
from sisense.data import Permission
import unittest


class PermissionTestCase(TestCase):

    def test_get(self):
        permission = self.sisense.permission
        permissions = permission.get(self.config['elasticube'])

        self.assertGreaterEqual(len(permissions), 1)

        for obj in permissions:
            self.assertEqual(type(obj), Permission)

        permissions = permission.get('Non existing elasticube')
        self.assertEqual(len(permissions), 1)
        self.assertEqual(permissions[0].permission, None)

    def test_add(self):
        self.sisense.permission.delete_all(self.config['elasticube'])

        self.sisense.permission.delete_all(self.config['elasticube'])
        old_permissions = self.sisense.permission.get(self.config['elasticube'])

        user = self.sisense.user.get(self.config['user_email'])
        self.sisense.permission.add(self.config['elasticube'], user._id, 'user', 'r')

        group = self.sisense.group.get('Dafiti')
        self.sisense.permission.add(self.config['elasticube'], group._id, 'group', 'r')

        new_permissions = self.sisense.permission.get(self.config['elasticube'])
        self.assertEqual(len(old_permissions) + 2, len(new_permissions))

        self.sisense.permission.delete_all(self.config['elasticube'])

    def test_delete_all(self):
        self.sisense.permission.delete_all(self.config['elasticube'])
        new_permissions = self.sisense.permission.get(self.config['elasticube'])

        self.assertEqual(len(new_permissions), 1)


if __name__ == '__main__':
    unittest.main()
