
import Token

class SimpleExpressionToken (Token.Token):
    def __init__(self, source, attribute):
        expression = (source + 1).getSimpleToken().getRest().getSimpleExpression().strip()
        setattr(self, attribute, expression)
        super().__init__(source[:expression.stop])

