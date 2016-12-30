import botocore
from scale.config import Config

class SecurityGroup(Config):
    def __init__(self, 
                    ec2_environment='default',
                    region='us-east-1',
                    group_id=None,
                    name=None, 
                    description=None,
                    vpc_id=None,
                    rules=[]):

        self.ec2_environment = ec2_environment
        self.region = region
        self.group_id = group_id
        self.name = name
        self.description = description
        self.vpc_id = vpc_id
        self.rules = rules

        super(SecurityGroup, self).__init__(ec2_environment=self.ec2_environment, region=self.region)


    def create(self):
        if self.name is None:
            self.log.error('You must set a SecurityGroup name!')
            exit(1)
        if self.description is None:
            self.log.error('You must set a SecurityGroup description!')
            exit(1)
            

        params = {
            'GroupName': self.name,
            'Description': self.description
        }

        ec2 = self.session.resource('ec2')

        try:
            response = ec2.create_security_group(**params)
            group_id = response.id
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
                self.log.error('Security Group [{sg}] already exists! '\
                                'I will attempt to update the rules'.format(sg=self.name))
                group_id = self.get_existing_sg_id()

        if len(self.rules) > 0:
            for rule in self.rules:
                self.add(group_id=group_id, ip=rule['IP'], from_port=rule['FromPort'],
                                to_port=rule['ToPort'], protocol=rule['Protocol'])

        return group_id

    def add(self, group_id, ip, from_port, to_port, protocol):
        ec2 = self.session.resource('ec2')
        security_group = ec2.SecurityGroup(group_id)

        params = {
            'IpProtocol': protocol,
            'FromPort': int(from_port),
            'ToPort': int(to_port),
            'IpRanges': [{'CidrIp': ip}]
        }

        try:
            security_group.authorize_ingress(GroupId=group_id, IpPermissions=[params])
        except botocore.exceptions.ClientError as e:
          if e.response['Error']['Code'] == 'InvalidPermission.Duplicate':
            self.log.error('Security Group Rule for [{sg}] [{ip}] Already exists!'.format(sg=group_id, ip=ip))


    def get_existing_sg_id(self, name=None):
        # Fetch the security group ID
        if name is None:
            name = self.name
        client = self.session.client('ec2')
        response = client.describe_security_groups(GroupNames=[name])

        return response['SecurityGroups'][0]['GroupId']


    def delete_all(self, group_id):
        ec2 = self.session.resource('ec2')
        security_group = ec2.SecurityGroup(group_id)

        client = self.session.client('ec2')
        response = client.describe_security_groups(GroupIds=[group_id])

        security_group.revoke_ingress(IpPermissions=response['SecurityGroups'][0]['IpPermissions'])


    def delete(self, group_id=None, name=None):
        if group_name is not None:
            self.session.delete_security_group(GroupName=name)

        if group_id is not None:
            self.session.delete_security_group(GroupId=group_id)
