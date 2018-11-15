
class TemplateTextNode (TemplateNode):
    def __init__(self, text):
        TemplateNode.__init__(self)
        self.text = text
        self.code = str(text)

    def render(self, output, namespace):
        output.append(self.code)
        return NoReturn()

