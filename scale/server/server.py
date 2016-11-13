from random import randint
from scale.config import Config
from scale.utilities.user_data import UserData

class Server(Config):

    def __init__(self, ec2_environment='default',
                            name=None,
                            dry_run=False,
                            ami='ami-06116566',
                            environment='stage',
                            tags=[],
                            disks=[],
                            user_data=None,
                            instance_type='m3.medium',
                            availability_zone=None,
                            keypair='~/.ssh/stage.pem',
                            ):
      self.name = name
      self.dry_run = dry_run
      self.ami = ami
      self.environment = environment
      self.availability_zone = availability_zone
      self.instance_type = instance_type
      self.disks = disks
      self.tags = tags
      self.user_data = user_data
      self.keypair = keypair

      super(Server, self).__init__(ec2_environment=ec2_environment)


    def bake(self):

        self.log.info('Starting server build')

        try:
          params = {
                'DryRun': self.dry_run,
                'ImageId': self.ami,
                'InstanceType': self.instance_type,
                'KeyName': self.keypair,
                'UserData': self.user_data,
                'SecurityGroupIds': self.security_group_ids,
                'MinCount': 1,
                'MaxCount': 1,
                'SubnetId': self.subnet,
                'Placement': {
                    'AvailabilityZone': '{region}{az}'.format(region=self.region,
                                            az=self.availability_zone)
                    }
                }
          instances = ec2.create_instances(**params)

          for i in instances:
            i.create_tags(Tags=self.tags)

        except Exception as e:

          self.log.error('Did not create instance due to [{e}]'.format(e=e))

