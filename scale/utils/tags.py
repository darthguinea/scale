class Tags(object):

    def __init__(self):
        self.TAGS = []


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
