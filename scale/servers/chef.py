from scale.server.server import Server

class ChefServer(Server):

  def __init__(self, ec2_environment='default',
                            name=None,
                            dry_run=False,
                            ami='ami-06116566',
                            environment='stage',
                            tags=[],
                            disks=[],
                            user_data=None,
                            instance_type='m3.medium',
                            availability_zone=None,
                            keypair='~/.ssh/stage.pem'):

    self.name = name
    self.dry_run = dry_run
    self.ami = ami
    self.environment = environment
    self.availability_zone = availability_zone
    self.instance_type = instance_type
    self.disks = disks
    self.tags = tags
    self.user_data = user_data
    self.keypair = keypair

    super(ChefServer, self).__init__(ec2_environment=ec2_environment)
  
  def bake(self):
    self.log.info('Building Chef Server!')
    super(ChefServer, self).bake()

