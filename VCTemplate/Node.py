
import sys

class Node (object):
    @classmethod
    def renderSequence(cls, context, sequence):
        for node in sequence:
            print("seq", node, context.locals, file=sys.stderr)
            r = node.render(context)
            print("/seq", node, context.locals, file=sys.stderr)
            if r is not None:
                return r
        return r

    def __init__(self, context):
        self.parse_context = context

