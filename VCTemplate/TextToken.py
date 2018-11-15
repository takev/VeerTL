
import Token
import TextNode

class TextToken (Token.Token):
    def __repr__(self):
        return repr(str(self.source))

    def getNode(self):
        return TextNode.TextNode(self.source)

