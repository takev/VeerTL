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
from . import ContinueNode
from . import BreakNode
from . import ReturnNode
        
class DoWhileNode (Node.Node):
    def __init__(self, context):
        super().__init__(context)
        self.sequence = []

    def __repr__(self):
        return "<dowhile %s: %s>" % (str(self.expression), repr(self.sequence))

    def append(self, node):
        self.sequence.append(node)

    def appendWhile(self, expression):
        self.expression = expression
        try:
            self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        except Exception as e:
            raise ParseError.ParseError(expression, "Could not compile Python code.") from e

    def render(self, context):
        while True:
            r = Node.Node.renderSequence(context, self.sequence)
            if isinstance(r, ContinueNode.ContinueNode):
                continue
            elif isinstance(r, BreakNode.BreakNode):
                break
            elif isinstance(r, ReturnNode.ReturnNode):
                return r

            try:
                result = context.eval(self.code)
            except Exception as e:
                raise RenderError.RenderError(self.expression, "Could not execute Python code.") from e

            if not result:
                break

        return None
        
