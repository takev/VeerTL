
import SimpleExpressionToken
import FlowControlToken
import IfNode

class IfToken (SimpleExpressionToken.SimpleExpressionToken, FlowControlToken.FlowControlToken):
    def __init__(self, source):
        super().__init__(source, "expression")

    def __repr__(self):
        return "<if %s>" % str(self.expression)

    def getNode(self, context):
        return IfNode.IfNode(context, self.expression)

