
import ParseError
import RenderContext
import sys

class ParseContext (object):
    def __init__(self):
        self.functions = {}

    def addFunction(self, name, func):
        old_func = self.functions.get(str(name), None)
        self.functions[str(name)] = func
        return old_func

    def makeRenderContext(self):
        _globals = self.functions.copy()
        return RenderContext.RenderContext(_globals=_globals, _locals=_globals)

