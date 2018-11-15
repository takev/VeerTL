
import SimpleExpressionToken
import ReturnNode

class ReturnToken (SimpleExpressionToken.SimpleExpressionToken):
    def __init__(self, source):
        super().__init__(source, "expression")

    def __repr__(self):
        return "<return %s>" % str(self.expression)

    def getNode(self):
        return ReturnNode.ReturnNode(self.expression)
