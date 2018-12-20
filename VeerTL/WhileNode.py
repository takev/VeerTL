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

from . import Node
from . import ContinueNode
from . import BreakNode
from . import ReturnNode

class WhileNode (Node.Node):
    def __init__(self, context, expression):
        super().__init__(context)
        self.expression = expression
        try:
            self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        except Exception as e:
            raise ParseError.ParseError(expression, "Could not compile Python expression.") from e

        self.sequence = []

    def __repr__(self):
        return "<while %s: %s>" % (str(self.expression), repr(self.sequence))

    def append(self, node):
        self.sequence.append(node)

    def render(self, context):
        if "loop" in context.locals:
            outer_loop = context.locals[loop]
        else:
            outer_loop = None

        i = 0
        while True:
            try:
                result = context.eval(self.code)
            except Exception as e:
                raise RenderError.RenderError(self.expression, "Could not evaluate Python expression.") from e

            if not result:
                break

            context["loop"] = LoopContext.LoopContext(i, None, None, outer_loop)

            r = Node.Node.renderSequence(context, self.sequence)

            # Reset "loop" variable in case we return.  
            if outer_loop is None:
                del context["loop"]
            else:
                context["loop"] = outer_loop

            if isinstance(r, ContinueNode.ContinueNode):
                continue
            elif isinstance(r, BreakNode.BreakNode):
                break
            elif isinstance(r, ReturnNode.ReturnNode):
                return r

            i += 1

        return None
        
