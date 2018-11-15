
import Token
import PlaceholderNode

class PlaceholderToken (Token.Token):
    def __init__(self, source):
        self.expression = (source + 2).getSimpleExpression("}")
        super().__init__(source[:self.expression.stop + 1])

    def __repr__(self):
        return "${" + str(self.expression) + "}"

    def getNode(self):
        return PlaceholderNode.PlaceholderNode(self.expression)

