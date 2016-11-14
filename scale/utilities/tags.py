class Tags(object):
  
    def __init__(self):
      self.TAGS = []


    def add(self, name=None, value=None):
      if name is not None:
        self.TAGS.append({'Key': name, 'Value': value})


    def printTags(self):
      for tag in self.get():
        print tag


    def get(self):
      return self.TAGS
