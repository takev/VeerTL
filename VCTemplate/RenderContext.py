
import sys
import inspect

class RenderContext (object):
    render_contexts = {}

    @classmethod
    def findRenderContext(self):
        for frame_info in inspect.stack()[2:]:
            if id(frame_info.frame) in RenderContext.render_contexts:
                return RenderContext.render_contexts[id(frame_info.frame)]

        else:
            raise RuntimeError("Could not find stack frame in RenderContext.render_contexts")


    def __init__(self, _globals, _locals):
        self.globals = _globals
        self.locals = _locals

        # For performance reasons insert the __builtins__.
        self.globals["__builtins__"] = globals()["__builtins__"]

        self.locals_stack = []
        self.output_stack = []
        self.output = []
        self.rendered_blocks = set()

    def __str__(self):
        return "".join(str(x) for x in self.output)

    def __repr__(self):
        return "<RenderContext globals=%s locals=%s output=%s>" % (
            repr(self.globals.keys()),
            repr(self.locals.keys()),
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

    def push(self, _locals):
        self.locals_stack.append(self.locals)
        self.locals = _locals
        self.output_stack.append(self.output.copy())
        self.output = []

    def pop(self):
        self.locals = self.locals_stack.pop()
        self.output = self.output_stack.pop()

    def eval(self, code):
        # Remember the current render_context so it can be found
        # by walking the stack frames.
        frame = inspect.currentframe()
        RenderContext.render_contexts[id(frame)] = self

        result = eval(code, self.globals, self.locals)

        del RenderContext.render_contexts[id(frame)]
        return result

    def exec(self, code):
        # Remember the current render_context so it can be found
        # by walking the stack frames.
        frame = inspect.currentframe()
        RenderContext.render_contexts[id(frame)] = self

        exec(code, self.globals, self.locals)

        del RenderContext.render_contexts[id(frame)]

    def append(self, value):
        # XXX Feed type parser when not self.output
        self.output.append(value)

    def callingBlock(self, name):
        if name in self.rendered_blocks:
            return False
        else:
            self.rendered_blocks.add(name)
            return True

