
import Token
import StatementNode

class StatementToken (Token.Token):
    def __init__(self, source):
        self.statement = (source + 2).getSimpleExpression()
        super().__init__(source[:self.statement.stop])

    def __repr__(self):
        return "<statement %s>" % str(self.statement)

    def getNode(self):
        return StatementNode.StatementNode(self.statement)

