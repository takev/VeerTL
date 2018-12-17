
import sys
import os.path

from . import SimpleExpressionToken
from . import SourceFile

class IncludeToken (SimpleExpressionToken.SimpleExpressionToken):
    def __init__(self, source):
        super().__init__(source, "path")

    def __repr__(self):
        return "<include %s>" % str(self.path)

    def getNode(self, context):
        from . import Parser

        # Calculate the new path relative to the path of the template
        # file that contains this include statement.
        new_path = self.path.includePath(str(self.path))

        source = SourceFile.SourceFile(new_path)
        template = Parser.parse(source, context=context)
        return template

