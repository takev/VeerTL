
class TemplateBlockToken (TemplateSimpleExpressionToken):
    def __init__(self, source):
        TemplateSimpleExpressionToken.__init__(self, source, "name")

    def __repr__(self):
        return "<block %s>" % str(self.name)

