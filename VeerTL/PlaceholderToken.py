
from . import Token
from . import PlaceholderNode

class PlaceholderToken (Token.Token):
    def __init__(self, source):
        self.expression = (source + 2).getSimpleExpression("}")
        super().__init__(source[:self.expression.stop + 1])

    def __repr__(self):
        return "%%{%s}" % str(self.expression)

    def getNode(self, context):
        return PlaceholderNode.PlaceholderNode(context, self.expression)

