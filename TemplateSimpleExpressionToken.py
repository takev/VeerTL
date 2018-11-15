
class TemplateSimpleExpressionToken (TemplateToken):
    def __init__(self, source, attribute):
        expression = (source + 1).getSimpleToken().getRest().getSimpleExpression()
        setattr(self, attribute, expression)
        TemplateToken.__init__(self, source[:expression.stop])

