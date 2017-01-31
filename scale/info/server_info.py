from scale.config import Config 
from scale.info.filters import Filters


class ServerInfo(Config):
    
    def __init__(self,
                    ec2_environment='default',
                    region='us-east-1',
                    filters=[]
                    ):

        self.amount = 0
        self.filters = filters

        super(ServerInfo, self).__init__(ec2_environment=ec2_environment, region=region)


    #
    # state: pending | running | shutting-down | terminated | stopping | stopped
    # 
    def instances(self):
        instances = []
        ec2 = self.session.resource('ec2')

        if len(self.filters) > 0:
            response = ec2.instances.filter(Filters=self.filters)
        else:
            response = ec2.instances.all()

        for i in response:
            self.amount += 1
            instances.append({
                'id': i.id,
                'tags': i.tags,
                'launch_time': i.launch_time,
                'az': i.placement['AvailabilityZone'],
                'arch': i.architecture,
                'network': {
                    'vpc_id': i.vpc_id,
                    'public_dns': i.public_dns_name,
                    'private_dns': i.private_dns_name,
                    'public_ip': i.public_ip_address,
                    'private_ip': i.private_ip_address,
                    'subnet_id': i.subnet_id,
                    }
            })

        return instances


    def count(self):
        return self.amount
