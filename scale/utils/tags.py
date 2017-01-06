from scale.config import Config


class Tags(Config):

    def __init__(self):
        self.TAGS = []

        super(Tags, self).__init__(ec2_environment='default', region='us-east-1')


    def add(self, name=None, value=None):
        if name is not None:
            for i in self.TAGS:
                if i['Key'] == name:
                    return
            self.TAGS.append({'Key': name, 'Value': value})


    def print_tags(self):
        for tag in self.get():
            print tag


    def get(self):
        return self.TAGS


    def get_instance_tags(self, instance_ids=[]):
        client = self.session.client('ec2')

        response = client.describe_tags(Filters=[{
                                   'Name': 'resource-id',
                                   'Values': instance_ids
                               }])
        return response['Tags']
