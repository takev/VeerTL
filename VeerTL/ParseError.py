

class ParseError (Exception):
    def __init__(self, source, msg):
        super().__init__(repr(source) + ":" + msg)        

