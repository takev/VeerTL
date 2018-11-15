
import ParseError
import RenderError
import parser
import Node

class StatementNode (Node.Node):
    def __init__(self, statement):
        super().__init__()
        self.statement = statement
        try:
            self.code = parser.suite(str(statement)).compile("<" + repr(statement) + ">")
        except Exception as e:
            raise ParseError.ParseError(statement, "Could not compile Python statement.") from e

    def __repr__(self):
        return "<statement %s>" % str(self.statement)

    def render(self, context):
        try:
            context.exec(self.code)
        except Exception as e:
            raise RenderError.RenderError(self.statement, "Could not execute Python statement.") from e

        return None

