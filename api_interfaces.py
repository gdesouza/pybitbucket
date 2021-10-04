

class ApiBase:

    def __init__(self, config):
        """
        :param config: dict
            dictionary containing the keys:
            - base_url (optional)
            - api_version (optional)
        """
        self.base_url = config.get('base_url', 'https://api.bitbucket.org')
        self.api_version = config.get('api_version', '2.0')

    def __str__(self):
        """Convert instance to string representation"""
        return self.api_url

    @property
    def api_url(self):
        return f'{self.base_url}/{self.api_version}'


class ApiRepositories(ApiBase):

    def __init__(self, config):
        assert 'owner' in config, 'Missing repository owner'
        assert 'repo_slug' in config, 'Missing repository name'
        
        self.owner = config.get('owner')
        self.repo_slug = config.get('repo_slug')
        super().__init__(config)
        

    def __str__(self):
        return self.api_url
    
    @property
    def api_url(self):
        return f'{super().api_url}/repositories/{self.owner}/{self.repo_slug}'


class ApiCommit(ApiRepositories):

    def __init__(self, config):
        assert 'revision' in config, 'Missing commit revision'
        
        self.revision = config.get('revision')
        super().__init__(config)

    def __str__(self):
        return self.api_url
    
    @property
    def api_url(self):
        return f'{super().api_url}/commit/{self.revision}'
