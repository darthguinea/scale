import os
from scale.config import Config


class UserData(Config):

    def __init__(self):

        super(UserData, self).__init__()


    def open(self, name=None):
        try:
            root = os.path.expanduser(name)
            file_data = open(root, 'r').read()

            self.log.info('Loading user data file [{0}]'.format(root))

            return file_data
        except:
            self.log.error('Could not load user data file [{0}]'.format(name))
            return None


    def create(self,
                    name='ubuntu',
                    params=None
                    ):

        root = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(root, '..', '..', 'data', name)

        if params is None:
            return open(path, 'r').read()
        else:
            return open(path, 'r').read().format(**params)
