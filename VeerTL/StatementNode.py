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

import parser

from . import ParseError
from . import RenderError
from . import Node

class StatementNode (Node.Node):
    def __init__(self, context, source, lines):
        super().__init__(context)
        self.source = source
        self.lines = lines
        try:
            self.code = parser.suite(lines).compile("<" + repr(source) + ">")
        except Exception as e:
            raise ParseError.ParseError(source, "Could not compile Python statement.") from e

    def __repr__(self):
        return "<statement %s>" % repr(self.lines)

    def render(self, context):
        try:
            context.exec(self.code)
        except Exception as e:
            raise RenderError.RenderError(self.source, "Could not execute Python statement.") from e

        return None

