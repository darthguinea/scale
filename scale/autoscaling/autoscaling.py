import time
import random
import botocore
from scale.config import Config


class Autoscaling(Config):

    def __init__(self,
                    ec2_environment='default',
                    region='us-east-1',
                    name=None,
                    ami='ami-d8bdebb8',
                    instance_type='t2.micro',
                    keypair='stage',
                    disks=[],
                    security_group_ids=[],
                    user_data=None,
                    desired_capacity=0,
                    min=0,
                    max=0,
                    azs=[]
                    ):

        self.ec2_environment = ec2_environment
        self.region = region
        self.name = name
        self.lc_name = '{name}-{v}'.format(name=self.name, v=int(time.time()))
        self.ami = ami
        self.instance_type = instance_type
        self.keypair = keypair
        self.disks = disks
        self.security_group_ids = security_group_ids
        self.user_data = user_data
        self.desired_capacity = desired_capacity
        self.min = min
        self.max = max
        self.azs = azs

        super(Autoscaling, self).__init__(ec2_environment=self.ec2_environment, region=self.region)
    
        self.configure()


    def configure(self):
        if self.name is None:
            self.log.error('You must set a name for your Autoscaling group!')
            exit(1)
        
        if len(self.azs) is 0:
            self.log.warn('No AZs configured, picking a random one'\
                            ' for region [{region}]'.format(region=self.region))
            zone = '{region}{az}'.format(region=self.region, az=random.sample(['a', 'c'], 1)[0])
            self.azs.append(zone)
            self.log.warn('I picked [{az}]'.format(az=zone))


    def create_launch_configuration(self):
        params = {
            'LaunchConfigurationName': self.lc_name,
            'ImageId': self.ami,
            'KeyName': self.keypair,
            'InstanceType': self.instance_type,
        }

        if len(self.disks) > 0:
            params['BlockDeviceMappings'] = self.disks

        if len(self.security_group_ids) > 0:
            params['SecurityGroups'] = self.security_group_ids

        if self.user_data is not None:
            params['UserData'] = self.user_data

        client = self.session.client('autoscaling')

        try:
            response = client.create_launch_configuration(**params)
            self.log.info('Created launch configuration [{lc}]'.format(lc=self.lc_name))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'AlreadyExists':
                self.log.warn('Launch Configuration arleady exists! Updating [{lc}]'\
                                    .format(lc=self.lc_name))
                self.log.info('Recreating LC with params')
            elif e.response['Error']['Code'] == 'ValidationError':
                self.log.error('AMI [{ami}] does not exist for this region!'\
                                .format(ami=self.ami))
                exit(1)


    def create_autoscaling_group(self):
        params = {
            'AutoScalingGroupName': self.name,
            'LaunchConfigurationName': self.lc_name,
            'MinSize': self.min,
            'MaxSize': self.max,
            'DesiredCapacity': self.desired_capacity,
            'AvailabilityZones': self.azs
        }


        client = self.session.client('autoscaling')

        try:
            client.create_auto_scaling_group(**params)
            self.log.info('Created autoscaling group [{asg}]'.format(asg=self.name))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'AlreadyExists':
                self.log.info('Could not create ASG [{name}] attempting to'\
                                ' update instead'.format(name=self.name))
                client.update_auto_scaling_group(**params)
                self.log.info('Created autoscaling group [{asg}]'.format(asg=self.name))


    def create(self):
        self.create_launch_configuration()
        self.create_autoscaling_group()
