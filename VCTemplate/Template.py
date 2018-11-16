
import sys

import Node

class Template (Node.Node):
    def __init__(self, context):
        super().__init__(context)
        self.sequence = []

    def __repr__(self):
        return "[%s]" % (", ".join(repr(x) for x in self.sequence))

    def append(self, node):
        self.sequence.append(node)

    def makeRenderContext(self):
        return self.parse_context.makeRenderContext()

    def render(self, context):
        return Node.Node.renderSequence(context, self.sequence)


