import os
from os.path import expanduser

class UserData(object):

    def __init__(self):
        pass

    def load(self, role='www', 
                environment='stage',
                encrypted_data_bag_file='~/.chef/encrypted_data_bag_secret',
                chef_key_file='~/.chef/chef-validator.pem',
                user_data_file='ubuntu-user-data',
                org='my-org',
                chef_url='chef.mydomain.com'):

        # Load user data from file:
        root = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(root, '..', '..', 'data', user_data_file)
        user_data = open(path, 'r').read()

        # Now load chef validator key:
        if chef_key_file is not None:
          chef_key = expanduser(chef_key_file)
          key = open(chef_key, 'r').read()
          encrypted_data_bag = expanduser(encrypted_data_bag_file) 
          encrypted_data_bag_secret = open(encrypted_data_bag, 'r').read()

          return user_data.format(role=role, 
                                    encrypted_data_bag=encrypted_data_bag_secret,
                                    validation_key=key,
                                    environment=environment,
                                    chef_url=chef_url,
                                    org=org)

        else:
          return user_data

