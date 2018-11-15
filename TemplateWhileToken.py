
class TemplateWhileToken (TemplateSimpleExpressionToken):
    def __init__(self, source):
        TemplateSimpleExpressionToken.__init__(self, source, "expression")

    def __repr__(self):
        return "<while %s>" % str(self.expression)

