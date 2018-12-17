
import SimpleExpressionToken

class ElifToken (SimpleExpressionToken.SimpleExpressionToken):
    def __init__(self, source):
        super().__init__(source, "expression")

    def __repr__(self):
        return "<elif %s>" % str(self.expression)

