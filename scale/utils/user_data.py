import os
from scale.config import Config


class UserData(Config):

    def __init__(self):

        super(UserData, self).__init__()


    def open(self, filename=None):
        try:
            root = os.path.expanduser(filename)
            file_data = open(root, 'r').read()

            self.log.info('Loading user data file [{0}]'.format(root))

            return file_data
        except:
            self.log.error('Could not load user data file [{0}]'.format(filename))
            return None


    def create(self,
                    user_file='ubuntu',
                    params=None
                    ):

        root = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(root, '..', '..', 'data', user_file)

        if params is None:
            return open(path, 'r').read()
        else:
            return open(path, 'r').read().format(**params)
