
import parser

import ParseError
import RenderError
import Node
import ContinueNode
import BreakNode
import ReturnNode
        
class DoWhileNode (Node.Node):
    def __init__(self):
        super().__init__()
        self.sequence = []

    def __repr__(self):
        return "<dowhile %s: %s>" % (str(self.expression), repr(self.sequence))

    def append(self, node):
        self.sequence.append(node)

    def appendWhile(self, expression):
        self.expression = expression
        try:
            self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        except Exception as e:
            raise ParseError.ParseError(expression, "Could not compile Python code.") from e

    def render(self, context):
        while True:
            r = Node.Node.renderSequence(context, self.sequence)
            if isinstance(r, ContinueNode.ContinueNode):
                continue
            elif isinstance(r, BreakNode.BreakNode):
                break
            elif isinstance(r, ReturnNode.ReturnNode):
                return r

            try:
                result = context.eval(self.code)
            except Exception as e:
                raise RenderError.RenderError(self.expression, "Could not execute Python code.") from e

            if not result:
                break

        return None
        
