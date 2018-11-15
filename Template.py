
class Template (TemplateNode):
    def __init__(self):
        self.sequence = []

    def append(self, node):
        self.sequence.append(node)

    def render(self, output, namespace):
        return TemplateNode.renderSequence(output, namespace, self.sequence)

