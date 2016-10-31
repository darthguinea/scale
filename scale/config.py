import logging
import ConfigParser
from os.path import expanduser
from boto3.session import Session

class Config(object):

    region_map = {
        'ap-northeast-1': 'apne1',
        'ap-southeast-1': 'apse1',
        'ap-southeast-2': 'apse2',
        'eu-central-1': 'euc1',
        'eu-west-1': 'euw1',
        'sa-east-1': 'sae1',
        'us-east-1': 'use1',
        'us-west-1': 'usw1',
        'us-west-2': 'usw2',
    }

    def __init__(self, config_files=None, ec2_environment='default'):
        self.ec2_environment = ec2_environment

        self.establish_logger()
        self.log.info('Loading Scale, using environment [{env}]'.format(env=ec2_environment))
        self.load_config_files(config_files=config_files)
        self.create_aws_session()

    def establish_logger(self):
        try:
            return self.log
        except:
            pass

        logging.basicConfig(format='[%(asctime)s] [%(levelname)s]: %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        logging.getLogger('botocore').setLevel(logging.CRITICAL)

        self.log = log

    def load_config_files(self, config_files=None):
        try:
            return self.config
        except:
            pass

        if config_files is None:
            home = expanduser("~")
            config_files = [ home + "/.aws/credentials", home + "/.aws/config" ]

        config = ConfigParser.ConfigParser()
        for file in config_files:
            self.log.info('Loading config file [{file}]'.format(file=file))
            config.read(file)

        self.config = config


    def create_aws_session(self):
        self.region = self.config.get(self.ec2_environment, 'region')

        self.session = Session(
            aws_access_key_id=self.config.get(self.ec2_environment, 'aws_access_key_id'),
            aws_secret_access_key=self.config.get(self.ec2_environment, 'aws_secret_access_key'),
            region_name=self.region
            )

