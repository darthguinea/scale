import random
from scale.config import Config


class Server(Config):
    def __init__(self, ec2_environment='default',
                    environment='stage',
                    ami='ami-d8bdebb8',
                    instance_type='t2.nano',
                    keypair=None,
                    region='us-east-1',
                    az=None,
                    dry_run=False):
        self.ec2_environment = ec2_environment
        self.environment = environment
        self.ami = ami
        self.instance_type = instance_type
        self.keypair = keypair
        self.region = region
        self.az = az
        self.dry_run = dry_run

        super(Server, self).__init__(ec2_environment=ec2_environment, region=self.region)

        self.configure()

    def configure(self):
        if self.az is None:
            self.az = random.sample(['a', 'b', 'c'], 1)[0]
            self.log.warn('AZ not set, picking random one [{az}]'.format(az=self.az))

        if self.keypair is None:
            self.log.error('No SSH key defined')
            exit(1)

    def bake(self):
        self.log.info('Starting server build')
    
        params = {
            'DryRun': self.dry_run,
            'ImageId': self.ami,
            'KeyName': self.keypair,
            'InstanceType': self.instance_type,
            'MinCount': 1,
            'MaxCount': 1
        }

        ec2 = self.session.resource('ec2')
        ec2.create_instances(DryRun=False, ImageId='ami-d8bdebb8', InstanceType='t2.nano', MinCount=1, MaxCount=1)
        

