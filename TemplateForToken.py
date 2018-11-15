
class TemplateForToken (TemplateToken):
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

        self.expression = source.getSimpleExpression()
        TemplateToken.__init__(self, token_source[:self.expression.stop])

    def __repr__(self):
        return "<for %s in %s>" % (", ".join(str(x) for x in self.names), str(self.expression))

