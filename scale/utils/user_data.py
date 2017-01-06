import os


class UserData(object):
    def __init__(self,
                    user_data_file='ubuntu',
                    org='my_org',
                    environment='stage',
                    enc_data_bag=None,
                    validation_key=None,
                    chef_url=None,
                    chef_role=None):

        self.user_data_file = user_data_file
        self.org = org
        self.environment = environment
        self.enc_data_bag = enc_data_bag
        self.validation_key = validation_key
        self.chef_url = chef_url
        self.chef_role = chef_role


    def get_enc_data_bag(self):
        pass


    def get_validation_key(self):
        pass


    def create(self):
        root = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(root, '..', '..', 'data', self.user_data_file)

        user_file = open(path, 'r').read()

        print root
        print path

        print user_file.format(role=self.chef_role,
                encrypted_data_bag=self.enc_data_bag,
                validation_key=self.validation_key,
                environment=self.environment,
                chef_url=self.chef_url,
                org=self.org
                )
