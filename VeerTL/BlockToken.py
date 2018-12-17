
from . import ParseError
from . import Token
from . import BlockNode

class BlockToken (Token.Token):
    def __init__(self, token_source):
        source = (token_source + 1).getSimpleToken().getRest()
        self.name = source.getSimpleToken()

        super().__init__(token_source[:self.name.stop])

    def __repr__(self):
        return "<block %s>" % (self.name)

    def getNode(self, context):
        return BlockNode.BlockNode(context, self.name)

