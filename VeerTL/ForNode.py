
import parser

import ParseError
import RenderError
import Node
import ReturnNode
import ContinueNode
import BreakNode
import LoopContext

class ForNode (Node.Node):
    def __init__(self, context, names, expression):
        super().__init__(context)
        self.names = [str(x) for x in names]
        self.expression = expression
        self.state = 0
        self.sequence = []
        self.else_sequence = []

        try:
            self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        except Exception as e:
            raise ParseError.ParseError(expression, "Could not compile Python expression.") from e

    def __repr__(self):
        s = "<for "
        s+= ", ".join(self.names)
        s+= " in %s: %s" % (str(self.expression), repr(self.sequence))
        if self.else_sequence:
            s+= " else %s" % repr(self.else_sequence)
        return s + ">"

    def append(self, node):
        if self.state == 0:
            self.sequence.append(node)
        else:
            self.else_sequence.append(node)

    def appendElse(self):
        if self.state != 0:
            raise ParseError(self.source, "Only one #else allowed on an #if statement.")

        self.state = 1

    def render(self, context):
        try:
            result = context.eval(self.code)
        except Exception as e:
            raise RenderError.RenderError(self.expression, "Could not evaluate Python expression.") from e

        if result:
            if "loop" in context.locals:
                outer = context.locals[loop]
            else:
                outer = None

            for i, values in enumerate(result):
                context["loop"] = ForNode.LoopContext(i, values, len(result), outer)

                if len(self.names) == 1:
                    context[self.names[0]] = values
                else:
                    for name, value in zip(self.names, values):
                        context[name] = value

                r = Node.Node.renderSequence(context, self.sequence)

                # Reset "loop" variable in case we return.  
                if outer is None:
                    del context["loop"]
                else:
                    context["loop"] = outer

                if isinstance(r, ContinueNode.ContinueNode):
                    continue
                elif isinstance(r, BreakNode.BreakNode):
                    break
                elif isinstance(r, ReturnNode.ReturnNode):

                    return r

        else:
            return Node.Node.renderSequence(context, self.else_sequence)

        return None

