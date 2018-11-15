
class TemplateForNode (TemplateNode):
    def __init__(self, names, expression):
        TemplateNode.__init__(self)
        self.names = [str(x) for x in names]
        self.expression = expression
        self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        self.state = 0
        self.sequence = []
        self.else_sequence = []

    def append(self, node):
        if self.state == 0:
            self.sequence.append(node)
        else:
            self.else_sequence.append(node)

    def appendElse(self):
        if self.state != 0:
            raise ParseError(self.source, "Only one #else allowed on an #if statement.")

        self.state = 1

    def render(self, output, namespace):
        try:
            result = eval(self.code, {}, namespace)
        except Exception, e:
            raise RenderError(self.expression, e)

        if result:
            for i, values in enumerate(result):
                namespace["_first"] = (i == 0)
                namespace["_last"] = (i == (len(result) - 1))

                if len(self.names) == 1:
                    namespace[self.names[0]] = values
                else:
                    for name, value in zip(self.names, values):
                        namespace[name] = value

                r = ASTNode.renderSequence(output, namespace, self.sequence)
                if isinstance(r, ContinueAST):
                    continue
                elif isinstance(r, BreakAST):
                    break
                else:
                    return r

        else:
            return TemplateNode.renderSequence(output, namespace, self.else_sequence)

        return NoReturn()

