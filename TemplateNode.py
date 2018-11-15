
class TemplateNode (object):
    def __init__(self):
        pass

    @classmethod
    def renderSequence(cls, output, namespace, sequence):
        for node in self.sequence:
            r = node.render(self, output, namespace)
            if not isinstance(NoReturn):
                return r
        return r

