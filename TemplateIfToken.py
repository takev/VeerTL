
class TemplateIfToken (TemplateSimpleExpressionToken):
    def __init__(self, source):
        TemplateSimpleExpressionToken.__init__(self, source, "expression")

    def __repr__(self):
        return "<if %s>" % str(self.expression)

