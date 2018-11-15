
import SimpleExpressionToken

class InherintToken (SimpleExpressionToken.SimpleExpressionToken):
    def __init__(self, source):
        super().__init__(source, "path")

    def __repr__(self):
        return "<inherint %s>" % str(self.path)

