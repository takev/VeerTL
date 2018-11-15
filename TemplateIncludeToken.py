
class TemplateIncludeToken (TemplateSimpleExpressionToken):
    def __init__(self, source):
        TemplateSimpleExpressionToken.__init__(self, source, "path")

    def __repr__(self):
        return "<include %s>" % str(self.path)

