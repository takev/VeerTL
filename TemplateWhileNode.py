
class TemplateWhileNode (TemplateNode):
    def __init__(self, expression):
        TemplateNode.__init__(self)
        self.expression = expression
        self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        self.sequence = []

    def append(self, node):
        self.sequence.append(node)

    def render(self, output, namespace):
        while True:
            try:
                result = eval(self.code, {}, namespace)
            except Exception, e:
                raise RenderError(self.expression, e)

            if not result:
                break

            r = TemplateNode.renderSequence(output, namespace, self.sequence)
            if isinstance(r, ContinueAST):
                continue
            elif isinstance(r, BreakAST):
                break
            else:
                return r

        return NoReturn()
        
