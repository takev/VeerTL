
import SimpleExpressionToken
import FlowControlToken
import WhileNode

class WhileToken (SimpleExpressionToken.SimpleExpressionToken, FlowControlToken.FlowControlToken):
    def __init__(self, source):
        super().__init__(source, "expression")

    def __repr__(self):
        return "<while %s>" % str(self.expression)

    def getNode(self):
        return WhileNode.WhileNode(self.expression)
