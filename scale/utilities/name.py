class Name(object):

    def __init__(self, environment='stage',
                    group='web',
                    ):

      self.environment = environment
      self.group = group


    def getServerName(self, format='{env[0]}-{group}'):

      return format.format(env=self.environment, 
                              group=self.group)
    
    
