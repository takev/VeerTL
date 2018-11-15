
class TemplateStatementNode (TemplateNode):
    def __init__(self, statement):
        TemplateNode.__init__(self)
        self.statement = statement
        self.code = parser.expr(str(statement)).compile("<" + repr(statement) + ">")

    def render(self, output, namespace):
        try:
            exec(self.code, {}, namespace)
        except Exception, e:
            raise RenderError(expression, e)

        return NoReturn()

