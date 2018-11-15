

class PostProcessResult (object):
    def __init__(self):
        self.functions = {}

    def __repr__(self):
        return "<PostProcessResult functions=%s>" % (
            repr(self.functions.keys())
        )

    def merge(self, other):
        self.functions.update(other.functions)

    def addFunction(self, name, func):
        self.functions[name] = func

