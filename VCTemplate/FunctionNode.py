
import sys
import parser

import RenderContext
import RenderError
import ReturnNode
import Node

class FunctionNode (Node.Node):
    def __init__(self, context, name, arguments):
        super().__init__(context)
        self.name = name
        self.arguments = [str(x) for x in arguments]
        self.sequence = []
        self.prior = context.addFunction(name, self)

    def __repr__(self):
        return "<function %s(%s): %s>" % (str(self.name), ", ".join(self.arguments), repr(self.sequence))

    def __call__(self, *args, **argd):
        try:
            context = RenderContext.RenderContext.findRenderContext()
        except Exception as e:
            raise RenderError.RenderError(self.name, "Expect _render_context to be in the global namespace.") from e

        if len(args) > len(self.arguments):
            raise RenderError.RenderError(self.name, "Unexpected number of arguments (%i), expected (%i)." % (len(args), len(self.arguments)))

        _locals = {}
        for name, value in zip(self.arguments, args):
            _locals[name] = value

        for name, value in argd.items():
            if name not in self.arguments:
                raise RenderError.RenderError(self.name, "Unexpected named argument (%s)." % (name))
            _locals[name] = value

        for name in self.arguments:
            if name not in _locals:
                raise RenderError.RenderError(self.name, "Missing argument (%s)." % (name))

        if self.prior is not None:
            _locals["prior"] = self.prior

        print("__call__", str(self.name), _locals, file=sys.stderr)
        context.push(_locals)

        r = Node.Node.renderSequence(context, self.sequence)
        if r is None:
            result = str(context)
        elif isinstance(r, ReturnNode.ReturnNode):
            result = r.result
        else:
            raise RenderError.RenderError(self.name, "Unexpected break or continue in function.")

        context.pop()
        print("/__call__", str(self.name), _locals, file=sys.stderr)
        return result

    def append(self, node):
        self.sequence.append(node)

    def render(self, context):
        return None


