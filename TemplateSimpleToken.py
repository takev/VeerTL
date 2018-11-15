
class TemplateSimpleToken (TemplateToken):
    def __init__(self, source):
        token_name = (source + 1).getSimpleToken()
        TemplateToken.__init__(self, source[:token_name.stop])

    def __repr__(self):
        return "<%s>" % str(self.source + 1)

