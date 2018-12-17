
import parser

from . import Node
from . import ContinueNode
from . import BreakNode
from . import ReturnNode

class WhileNode (Node.Node):
    def __init__(self, context, expression):
        super().__init__(context)
        self.expression = expression
        try:
            self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        except Exception as e:
            raise ParseError.ParseError(expression, "Could not compile Python expression.") from e

        self.sequence = []

    def __repr__(self):
        return "<while %s: %s>" % (str(self.expression), repr(self.sequence))

    def append(self, node):
        self.sequence.append(node)

    def render(self, context):
        while True:
            try:
                result = context.eval(self.code)
            except Exception as e:
                raise RenderError.RenderError(self.expression, "Could not evaluate Python expression.") from e

            if not result:
                break

            r = Node.Node.renderSequence(context, self.sequence)
            if isinstance(r, ContinueNode.ContinueNode):
                continue
            elif isinstance(r, BreakNode.BreakNode):
                break
            elif isinstance(r, ReturnNode.ReturnNode):
                return r

        return None
        
