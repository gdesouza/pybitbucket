import unittest
from credentials import Credentials

class TestPybitbucket(unittest.TestCase):

    def setUp(self):
        pass

    def testCredentials(self):
        config = {
            'username': 'test',
            'password': '12345'
        }

        credentials = Credentials(config)
        self.assertEqual(credentials.username, config['username'])
        self.assertEqual(credentials.password, config['password'])
        self.assertEqual(credentials.tuple, (config['username'], config['password']))

    def testUsernameNotSet(self):
        config = {
            'password': '12345'
        }

        with self.assertRaises(AssertionError) as context:
            credentials = Credentials(config)

        self.assertTrue('Missing username for credentials' in str(context.exception))
        self.assertIsNone(credentials)

    def testPasswordNotSet(self):
        config = {
            'username': 'test'
        }

        with self.assertRaises(AssertionError) as context:
            credentials = Credentials(config)

        self.assertTrue('Missing password for credentials' in str(context.exception))



if __name__ == '__main__':
    unittest.main()