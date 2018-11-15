
import Token
import StatementNode

class StatementToken (Token.Token):
    def __init__(self, source):
        statement = (source + 2).getSimpleExpression()
        self.lines = [str(statement)]
        super().__init__(source[:statement.stop])

    def __str__(self):
        leading_spaces = len(self.lines[0]) - len(self.lines[0].lstrip())
        return "\n".join(x[leading_spaces:] for x in self.lines) + "\n"

    def __repr__(self):
        return "<statement %s>" % repr(str(self))

    def getNode(self):
        return StatementNode.StatementNode(self.source, str(self))

    def merge(self, other):
        if isinstance(other, StatementToken):
            self.lines.append(other.lines[0])
            return True
        else:
            return False
