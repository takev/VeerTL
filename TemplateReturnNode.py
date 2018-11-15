
class TemplateReturnNode (TemplateNode):
    def __init__(self, expression):
        TemplateNode.__init__(self)
        self.expression = expression
        self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")

    def render(self, output, namespace):
        try:
            result = eval(self.code, {}, namespace)
        except Exception, e:
            raise RenderError(self.expression, e)

        return result

