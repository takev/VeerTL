
import parser

import RenderContext
import RenderError
import ReturnNode
import Node

class MethodNode (Node.Node):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.sequence = []
        self.super = None

    def __repr__(self):
        return "<method %s: %s>" % (str(self.name), repr(self.sequence))

    def __call__(self, *args, **argd):
        _locals["super"] = self.super

        context = RenderContext.RenderContext(_locals=_locals)
        r = Node.Node.renderSequence(context, self.sequence)
        if r is None:
            result = str(context)
        elif isinstance(r, ReturnNode.ReturnNode):
            result = r.result
        else:
            raise RenderError.RenderError(self.name, "Unexpected break or continue in function.")

        return result

    def append(self, node):
        self.sequence.append(node)

    def render(self, context):
        return None
