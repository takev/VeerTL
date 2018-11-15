
class TemplatePlaceholderToken (TemplateToken):
    def __init__(self, source):
        self.expression = (source + 2).getSimpleExpression("}")
        TemplateToken.__init__(self, source[:self.expression.stop + 1])

    def __repr__(self):
        return "${" + str(self.expression) + "}"

