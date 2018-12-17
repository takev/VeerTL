# Template Language for code generation.
# Copyright (C) 2018  Tjienta Vara
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

