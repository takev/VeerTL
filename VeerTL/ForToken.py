
from . import Token
from . import FlowControlToken
from . import ForNode

class ForToken (Token.Token, FlowControlToken.FlowControlToken):
    def __init__(self, token_source):
        source = (token_source + 1).getSimpleToken().getRest()

        self.names = []
        while True:
            name = source.getSimpleToken()
            self.names.append(name)
            source = name.getRest()

            comma = source.getSimpleToken()
            source = comma.getRest()
            if str(comma) == ",":
                continue
            elif str(comma) == "in":
                break
            else:
                raise ParseError(comma, "Unexpected string '%s'." % str(comma))

        self.expression = source.getSimpleExpression().strip()
        super().__init__(token_source[:self.expression.stop])

    def __repr__(self):
        return "<for %s in %s>" % (", ".join(str(x) for x in self.names), str(self.expression))

    def getNode(self, context):
        return ForNode.ForNode(context, self.names, self.expression)

