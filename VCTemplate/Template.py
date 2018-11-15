
import sys

import Node
import RenderContext
import PostProcessResult

class Template (Node.Node):
    def __init__(self):
        super().__init__()
        self.sequence = []

    def __repr__(self):
        return "[%s]" % (", ".join(repr(x) for x in self.sequence))

    def append(self, node):
        self.sequence.append(node)

    def makeRenderContext(self):
        _globals = self.result.functions.copy()
        return RenderContext.RenderContext(_globals=_globals, _locals={})

    def render(self, context):
        return Node.Node.renderSequence(context, self.sequence)

    def postProcess(self, result=None):
        if result is None:
            result = PostProcessResult.PostProcessResult()
        else:
            result = result

        for node in self.sequence:
            node.postProcess(result)

        self.result = result
        return result

