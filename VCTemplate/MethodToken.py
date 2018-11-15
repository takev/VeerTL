
import SimpleExpressionToken
import MethodNode

class MethodToken (SimpleExpressionToken.SimpleExpressionToken):
    def __init__(self, source):
        super().__init__(source, "name")

    def __repr__(self):
        return "<block %s>" % str(self.name)

    def getNode(self):
        return MethodNode.MethodNode(self.name)

