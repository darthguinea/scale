import random
from scale.config import Config
from scale.utilities.tags import Tags
from scale.utilities.user_data import UserData

class Server(Config):

    def __init__(self, ec2_environment='default',
                            name=None,
                            dry_run=False,
                            ami='ami-d8bdebb8',
                            environment='stage',
                            chef_role=None,
                            tags=[],
                            disks=[],
                            user_data='',
                            instance_type='m3.medium',
                            security_group_ids=[],
                            region=None,
                            availability_zone=None,
                            security_group=None,
                            keypair='~/.ssh/stage.pem',
                            ):
        self.name = name
        self.dry_run = dry_run
        self.ami = ami
        self.environment = environment
        self.chef_role = chef_role
        self.region = region
        self.availability_zone = availability_zone
        self.instance_type = instance_type
        self.disks = disks
        self.tags = tags
        self.user_data = user_data
        self.security_group_ids = security_group_ids
        self.keypair = keypair

        self.configure()

        super(Server, self).__init__(ec2_environment=ec2_environment)


    def configure(self):
        if self.availability_zone is None:
            self.availability_zone = random.sample(['a', 'b', 'c'], 1)[0]
        

    def bake(self):
        self.log.info('Starting server build')

        try:
            params = {
                'DryRun': self.dry_run,
                'ImageId': self.ami,
                'InstanceType': self.instance_type,
                'KeyName': self.keypair,
                'MinCount': 1,
                'MaxCount': 1,
                'Placement': {
                    'AvailabilityZone': '{region}{az}'.format(region=self.region,
                                                                az=self.availability_zone)
                }
            }


            ec2 = self.session.resource('ec2')
            instances = ec2.create_instances(**params)

            for i in instances:
                i.create_tags(Tags=self.tags)

        except Exception as e:
            self.log.error('Did not create instance due to [{e}]'.format(e=e))

