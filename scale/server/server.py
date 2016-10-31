from scale.config import Config
from scale.utilities.user_data import UserData

class Server(Config):

    def __init__(self, ec2_environment='default',
                            ami='ami-06116566',
                            environment='stage',
                            tags=[],
                            dry_run=False,
                            instance_type='m3.medium',
                            availability_zone=None,
                            ):

        super(Server, self).__init__(ec2_environment=ec2_environment)
        

    def bake(self):
      self.log.info('Building server...')

