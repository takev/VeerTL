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

from . import Token
from . import IgnoreWhiteSpaceNode

class IgnoreWhiteSpaceToken (Token.Token):
    def __init__(self, source):
        statement = (source + 2).getWhiteSpace()
        self.lines = [str(statement)]
        super().__init__(source[:statement.stop])

    def __str__(self):
        leading_spaces = len(self.lines[0]) - len(self.lines[0].lstrip())
        return "\n".join(x[leading_spaces:] for x in self.lines) + "\n"

    def __repr__(self):
        return "<ignore-white-space %s>" % repr(str(self))

    def getNode(self, context):
        return IgnoreWhiteSpaceNode.IgnoreWhiteSpaceNode(context, self.source, str(self))

