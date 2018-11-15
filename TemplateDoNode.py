        
class TemplateDoNode (TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)
        self.sequence = []

    def append(self, node):
        self.sequence.append(node)

    def appendWhile(self, expression)
        self.expression = expression
        self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")

    def render(self, output, namespace):
        while True:
            r = TemplateNode.renderSequence(output, namespace, self.sequence)
            if isinstance(r, ContinueAST):
                continue
            elif isinstance(r, BreakAST):
                break
            else:
                return r

            try:
                result = eval(self.code, {}, namespace)
            except Exception, e:
                raise RenderError(self.expression, e)

            if not result:
                break

        return NoReturn()
        
