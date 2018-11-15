
class TemplateStatementToken (TemplateToken):
    def __init__(self, source):
        self.statement = (source + 2).getSimpleExpression()
        TemplateToken.__init__(self, source[:self.statement.stop])

    def __repr__(self):
        return "<statement %s>" % str(self.statement)

