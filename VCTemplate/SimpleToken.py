
import Token

class SimpleToken (Token.Token):
    def __init__(self, source):
        token_name = (source + 1).getSimpleToken()
        super().__init__(source[:token_name.stop])

    def __repr__(self):
        return "<%s>" % str(self.source + 1).strip()

