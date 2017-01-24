import time
import string
from scale.config import Config

class DNS(Config):

    def __init__(self,
                    ec2_environment='default',
                    region='us-east-1',
                    ):

        self.ec2_environment = ec2_environment
        self.region = region

        super(DNS, self).__init__(ec2_environment=self.ec2_environment, region=self.region)
    

    def create_zone(self, name=None, vpc_id=None, private=True):
        if name is None:
            return

        params = {
            'Name': name,
            'CallerReference': str(int(time.time())),
            'HostedZoneConfig': {
                'Comment': '',
                'PrivateZone': private
            },
        }

        if vpc_id is not None:
            vpc = {
                'VPCRegion': self.region,
                'VPCId': vpc_id 
            }
            params['VPC'] = vpc

        self.log.info('Creating hosted zone [{params}]'.format(params=params))

        if not self.zone_exists(name=name, private=private):
            client = self.session.client('route53')
            client.create_hosted_zone(**params)


    def zone_exists(self, name=None, private=False):
        if name is None:
            return

        client = self.session.client('route53')

        zones = client.list_hosted_zones()

        self.log.info('searching for {name}. and {private}'\
                            .format(name=name, private=private))

        for zone in zones['HostedZones']:
            if zone['Name'] == '{name}.'.format(name=name) and \
                    private == zone['Config']['PrivateZone']:
                self.log.warn('Zone [{name}.] Private [{private}] exists already'\
                                .format(name=name, private=private))
                return True
        return False


    def get_zone_data(self, name=None, private=False):
        client = self.session.client('route53')
        zones = client.list_hosted_zones()

        for zone in zones['HostedZones']:
            if zone['Name'] == '{name}.'.format(name=name) and \
                    private == zone['Config']['PrivateZone']:
                self.log.info('get_zone_data found zone [{zone}] '\
                                'private[{private}]'.format(zone=zone,
                                                        private=private))
                return zone


    def find_hosted_zone_id(self, name=None, private=False):
        arr = name.split('.')
        tmp = arr
        
        for a in arr:
            tmp.pop(0)
            self.log.info('Testing [{0}], is hosted zone?'\
                            .format(string.join(tmp, '.')))
            response = self.get_zone_data(name=string.join(tmp, '.'), private=private)

            try:
                self.log.info('[{0}] is hosted zone '\
                                'returning HZ id[{1}] '\
                                .format(string.join(tmp, '.'), 
                                response['Id']))
                return response['Id']
            except:
                pass
        
        return None


    def add(self, 
                name=None,
                address=None,
                type='A',
                location='172.32.0.1',
                weight=10,
                ttl=300,
                private=False,
                comment=None,
                ):

        if name is None:
            self.log.error('dns [name] cannot be blank when adding records')
            exit(1)

        if address is None:
            self.log.error('dns [address] cannot be blank when adding records')
            exit(1)
            
        if private is True:
            self.log.info('Private hosted zone')

        id = None
        id = self.find_hosted_zone_id(name, private)

        if id is None:
            self.log.error('No hosted zone found for [{name}]'\
                            .format(name=name))

        params = {
            'HostedZoneId': id,
            'ChangeBatch':{
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': name,
                        'ResourceRecords': [
                            {
                                'Value': address
                            }
                        ],
                        'Type': type,
                        'TTL': ttl
                    }
                }
            ]
            }       
        }

        if comment is not None:
            params['Comment'] = comment

        client = self.session.client('route53')
        client.change_resource_record_sets(**params)


