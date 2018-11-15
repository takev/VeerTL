
import parser

import ParseError
import RenderError
import Node

class ReturnNode (Node.Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression
        try:
            self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        except Exception as e:
            raise ParseError.ParseError(expression, "Could not compile Python expression.") from e

    def __repr__(self):
        return "<return %s>" % str(self.expression)

    def render(self, context):
        try:
            self.result = context.eval(self.code)
        except Exception as e:
            raise RenderError.RenderError(self.expression, "Could not evaluate Python expression.") from e

        return self

