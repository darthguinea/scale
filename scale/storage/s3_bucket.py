import botocore
from scale.config import Config


class S3Bucket(Config):

    def __init__(self,
                    ec2_environment='default',
                    name=None
                    ):

        self.ec2_environment = ec2_environment
        self.name = name
        
        super(S3Bucket, self).__init__(ec2_environment=ec2_environment)

        self.s3 = self.session.resource('s3')


    def upload_files(self, name=None, files=[], location=''):
        if name is None:
            name = self.name
        if name is None:
            self.log.error('You must set a bucket name!')
            return

        # If the last charecter of the loction is / then
        # remove it if the length is longer than one
        loc = location
        if location != '' and location[0] == '/':
            loc = location[1:]
        if location != ''\
                and location[-1] != '/' and len(location) > 1:
            loc = '{l}/'.format(l=location)

        for f in files:
            try:
                response = self.s3.Object(name, '{loc}{fn}'\
                                            .format(loc=loc, fn=f)).\
                                                put(Body=open('{fn}'\
                                                    .format(fn=f), 'rb'))
            except IOError:
                self.log.error('Could not find local file [{f}]'.format(f=f))


    def delete_files(self, name=None, files=[]):
        if name is None:
            name = self.name
        if name is None:
            self.log.error('No bucket name found')
            return

        for f in files:
            self.s3.Object(name, f).delete()


    def delete_bucket(self, name=None):
        if name is None:
            name = self.name
        if name is None:
            self.log.error('No bucket name found, cannot delete bucket!')
            return

        bucket = self.s3.Bucket(name)
        try:
            self.s3.meta.client.head_bucket(Bucket=name)

            for key in bucket.objects.all():
                key.delete()

            bucket.delete()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'Forbidden':
                self.log.error('Unable to delete or find bucket [{bucket}]'\
                                    .format(bucket=name))


    def create_bucket(self, name=None):
        if name is None:
            name = self.name
        if name is None:
            self.log.error('Cannot create bucket with no name')
            return
        
        try:
            self.s3.create_bucket(Bucket=name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyExists':
                self.log.error('Unable to create bucket [{name}], another AWS '\
                                'user may own this already, the bucket name must '\
                                'be unique'.format(name=name))
                return
