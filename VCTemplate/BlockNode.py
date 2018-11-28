
import sys
import parser

import FunctionNode
import ParseError

class BlockNode (FunctionNode.FunctionNode):
    def __init__(self, context, name):
        super().__init__(context, name, [])

        expression = "%s()" % str(name)
        try:
            self.code = parser.expr(expression).compile("<" + expression + ">")
        except Exception as e:
            raise ParseError.ParseError(expression, "Could not compile Python expression.") from e


    def render(self, context):
        if context.callingBlock(str(self.name)):
            try:
                result = context.eval(self.code)
            except Exception as e:
                raise RenderError.RenderError(self.expression, "Could not evaluate Python expression.") from e

            context.append(result)

        return None

