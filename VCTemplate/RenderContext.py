

class RenderContext (object):
    def __init__(self, _globals=None, _locals={}):
        if _globals is None:
            self.globals = globals()
        else:
            self.globals = _globals

        # For performance reasons insert the __builtins__.
        self.globals["__builtins__"] = globals()["__builtins__"]

        self.locals = _locals
        self.output = []

    def __str__(self):
        return "".join(str(x) for x in self.output)

    def __repr__(self):
        return "<RenderContext globals=%s locals=%s output=%s>" % (
            repr(self.globals),
            repr(self.locals),
            repr(self.output)
        )

    def __setitem__(self, name, value):
        self.locals[name] = value

    def __getitem__(self, name):
        if name in self.locals:
            return self.locals[name]
        return self.globals[name]

    def __delitem__(self, name):
        if name in self.locals:
            del self.locals[name]
        if name in self.globals:
            del self.globals[name]

    def eval(self, code):
        return eval(code, self.globals, self.locals)

    def exec(self, code):
        exec(code, self.globals, self.locals)

    def append(self, value):
        self.output.append(value)

