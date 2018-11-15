
import ParseError
import Token
import FunctionNode

class FunctionToken (Token.Token):
    def __init__(self, token_source):
        source = (token_source + 1).getSimpleToken().getRest()

        self.name = source.getSimpleToken()
        source = self.name.getRest()

        open_bracket = source.getSimpleToken()
        source = open_bracket.getRest()
        if str(open_bracket) != "(":
            raise ParseError.ParseError(open_bracket, "Expecting open bracket '(', but got '%s'." % str(open_bracket))

        self.arguments = []
        while True:
            name = source.getSimpleToken()
            if str(name) == ")":
                break

            self.arguments.append(name)
            source = name.getRest()

            comma = source.getSimpleToken()
            source = comma.getRest()
            if str(comma) == ",":
                continue
            elif str(comma) == ")":
                break
            else:
                raise ParseError.ParseError(comma, "Unexpected string '%s'." % str(comma))

        super().__init__(token_source[:comma.stop])

    def __repr__(self):
        return "<function %s(%s)>" % (self.name, ", ".join(str(x) for x in self.names))

    def getNode(self):
        return FunctionNode.FunctionNode(self.name, self.arguments)

