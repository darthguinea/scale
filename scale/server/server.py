import random
import botocore
from scale.config import Config


class Server(Config):
    def __init__(self, ec2_environment='default',
                    environment='stage',
                    ami='ami-d8bdebb8',
                    instance_type='t2.nano',
                    keypair=None,
                    region='us-east-1',
                    az=None,
                    name=None,
                    tags=[],
                    disks=[],
                    dry_run=False):
        self.ec2_environment = ec2_environment
        self.environment = environment
        self.ami = ami
        self.instance_type = instance_type
        self.keypair = keypair
        self.region = region
        self.az = az
        self.name = name
        self.tags = tags
        self.disks = disks
        self.dry_run = dry_run

        super(Server, self).__init__(ec2_environment=ec2_environment, region=self.region)

    def configure(self):
        if self.az is None:
            self.az = random.sample(['a', 'b', 'c'], 1)[0]
            self.log.warn('AZ not set, picking random one [{az}]'.format(az=self.az))

        if self.keypair is None:
            self.log.error('No SSH key defined')
            exit(1)

        if self.name is not None:
            self.tags.append({'Key': 'Name', 'Value': self.name})


    def create(self):
        self.log.info('Starting server build')

        self.configure()
    
        params = {
            'ImageId': self.ami,
            'KeyName': self.keypair,
            'InstanceType': self.instance_type,
            'MinCount': 1,
            'MaxCount': 1,
            'DryRun': self.dry_run
        }

        if len(self.disks) > 0:
            params['BlockDeviceMappings'] = self.disks

        ec2 = self.session.resource('ec2')

        try:
            instances = ec2.create_instances(**params)

            if len(self.tags) > 0:
                for instance in instances:
                    instance.create_tags(Tags=self.tags)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'InvalidAMIID.NotFound':
                self.log.error('AMI [{ami}] not found, AMIs are region based '\
                                    'try changing region or updating your AMI image'.format(ami=self.ami))
            else:
                self.log.error('Unexpected error: {e}'.format(e=e))

