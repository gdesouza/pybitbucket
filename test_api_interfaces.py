import unittest
from api_interfaces import ApiBase, ApiCommit, ApiRepositories

class TestApiInterfaces(unittest.TestCase):

    def setUp(self):
        self.config = {
            'base_url': 'https://some.api.url',
            'api_version': '1.0',
            'owner': 'someone',
            'repo_slug': 'some_repo',
            'revision': 'some_revision'
        }

    def testApiBaseDefaultValues(self):
        config = {}
        api = ApiBase(config)
        self.assertEqual(api.base_url, 'https://api.bitbucket.org')
        self.assertEqual(api.api_version, '2.0')
        self.assertEqual(api.api_url, 'https://api.bitbucket.org/2.0')
        self.assertEqual(api.api_url, str(api))

    def testApiBase(self):
        config = self.config
        api = ApiBase(config)
        self.assertEqual(api.base_url, config['base_url'])
        self.assertEqual(api.api_version, config['api_version'])
        self.assertEqual(api.api_url, f"{config['base_url']}/{config['api_version']}")
        self.assertEqual(api.api_url, str(api))

    def testApiRepository(self):
        config = self.config
        api = ApiRepositories(config)
        self.assertEqual(api.base_url, config['base_url'])
        self.assertEqual(api.api_version, config['api_version'])
        self.assertEqual(api.owner, config['owner'])
        self.assertEqual(api.repo_slug, config['repo_slug'])
        self.assertEqual(api.api_url, f"{config['base_url']}/{config['api_version']}/repositories/{config['owner']}/{config['repo_slug']}")
        self.assertEqual(api.api_url, str(api))
        
    def testApiCommit(self):
        config = self.config
        api = ApiCommit(config)
        self.assertEqual(api.base_url, config['base_url'])
        self.assertEqual(api.api_version, config['api_version'])
        self.assertEqual(api.owner, config['owner'])
        self.assertEqual(api.repo_slug, config['repo_slug'])
        self.assertEqual(api.revision, config['revision'])
        self.assertEqual(api.api_url, f"{config['base_url']}/{config['api_version']}/repositories/{config['owner']}/{config['repo_slug']}/commit/{config['revision']}")
        self.assertEqual(api.api_url, str(api))


if __name__ == '__main__':
    unittest.main()