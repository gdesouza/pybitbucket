class Credentials():
    
    def __init__(self, config):
        assert 'username' in config, 'Missing username for credentials'
        assert 'password' in config, 'Missing password for credentials'

        self.username = config['username']
        self.password = config['password']

    @property
    def tuple(self):
        return (self.username, self.password)
