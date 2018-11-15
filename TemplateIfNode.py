        
class TemplateIfNode (TemplateNode):
    def __init__(self, expression):
        TemplateNode.__init__(self)
        self.state = 0
        self.expression_sequence = [(
            expression,
            parser.expr(str(expression)).compile("<" + repr(expression) + ">")
            []
        )]
        self.else_sequence = []

    def append(self, node):
        if self.state == 0:
            sequence = self.expression_sequence[-1][1]
            sequence.append(node)
        else:
            self.else_sequence.append(node)

    def appendElif(self, expression):
        self.expression_sequence.append((
            expression,
            parser.expr(str(expression)).compile("<" + repr(expression) + ">")
            []
        ))

    def appendElse(self):
        if self.state != 0:
            raise ParseError(self.source, "Only one #else allowed on an #if statement.")

        self.state = 1

    def render(self, output, namespace):
        for expression, code, sequence in self.expression_sequence:
            try:
                result = eval(code, {}, namespace)
            except Exception, e:
                raise RenderError(expression, e)

            if result:
                return TemplateNode.renderSequence(output, namespace, sequence)
        else:
            return TemplateNode.renderSequence(output, namespace, self.else_sequence)

