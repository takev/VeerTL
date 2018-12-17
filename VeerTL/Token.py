
class Token (object):
    def __init__(self, source):
        from . import PlaceholderToken
        from . import TextToken
        if isinstance(self, PlaceholderToken.PlaceholderToken) or isinstance(self, TextToken.TextToken):
            self.source = source
        else:
            self.source = source.expand()

    def getRest(self):
        return self.source.getRest()

    def merge(self, other):
        return False
