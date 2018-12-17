
import parser

from . import ParseError
from . import RenderError
from . import Node

class StatementNode (Node.Node):
    def __init__(self, context, source, lines):
        super().__init__(context)
        self.source = source
        self.lines = lines
        try:
            self.code = parser.suite(lines).compile("<" + repr(source) + ">")
        except Exception as e:
            raise ParseError.ParseError(source, "Could not compile Python statement.") from e

    def __repr__(self):
        return "<statement %s>" % repr(self.lines)

    def render(self, context):
        try:
            context.exec(self.code)
        except Exception as e:
            raise RenderError.RenderError(self.source, "Could not execute Python statement.") from e

        return None
