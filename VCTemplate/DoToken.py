
import SimpleToken
import FlowControlToken
import DoWhileNode

class DoToken (SimpleToken.SimpleToken, FlowControlToken.FlowControlToken):
    def getNode(self):
        return DoWhileNode.DoWhileNode()

