
class TemplateToken (object):
    def __init__(self, source):
        self.source = source

    def getRest(self):
        return self.source.getRest()

