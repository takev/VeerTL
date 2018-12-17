
import sys

from . import Token
from . import TextNode

class TextToken (Token.Token):
    def __repr__(self):
        return repr(str(self.source))

    def __len__(self):
        return len(self.source)

    def __bool__(self):
        return len(self) > 0

    def getNode(self, context):
        return TextNode.TextNode(context, self.source)

    def merge(self, other):
        if isinstance(other, TextToken):
            self.source.merge(other.source)
            return True
        else:
            return False

