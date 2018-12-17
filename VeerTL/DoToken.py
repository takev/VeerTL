
from . import SimpleToken
from . import FlowControlToken
from . import DoWhileNode

class DoToken (SimpleToken.SimpleToken, FlowControlToken.FlowControlToken):
    def getNode(self, context):
        return DoWhileNode.DoWhileNode(context)

