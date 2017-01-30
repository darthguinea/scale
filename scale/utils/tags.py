class Tags:

    def __init__(self):
        self.current = 0
        self.TAGS = []

    
    def exists(self, name):
        for i in self.TAGS:
            if i['Key'] == name:
                return True
        return False


    def add(self, name=None, value=None):
        if name is None:
            return

        if self.exists(name):
            new_list = []
            for item in self.TAGS:
                if item['Key'] == name:
                    item['Value'] = value
                new_list.append(item)
                
            self.TAGS = new_list
            return

        self.TAGS.append({'Key': name, 'Value': value})


    def get(self):
        return self.TAGS


    def __len__(self):
        return len(self.TAGS)


    def __iter__(self):
        return self


    def next(self):
        if self.current >= len(self.TAGS):
            raise StopIteration
        else:
            self.current += 1
            return self.TAGS[self.current -1]

