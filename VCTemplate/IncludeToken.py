
import sys
import os.path
import SimpleExpressionToken
import SourceFile

class IncludeToken (SimpleExpressionToken.SimpleExpressionToken):
    cache = {}

    def __init__(self, source):
        super().__init__(source, "path")

    def __repr__(self):
        return "<include %s>" % str(self.path)

    def getNode(self):
        import Parser

        # Calculate the new path relative to the path of the template
        # file that contains this include statement.
        new_path = self.path.includePath(str(self.path))

        if new_path in IncludeToken.cache:
            return InclueToken.cache[new_path]

        else:
            source = SourceFile.SourceFile(new_path)
            template = Parser.parse(source)
            IncludeToken.cache[new_path] = template
            return template

