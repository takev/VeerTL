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
from . import ReturnNode
from . import ContinueNode
from . import BreakNode
from . import LoopContext

class ForNode (Node.Node):
    def __init__(self, context, names, expression):
        super().__init__(context)
        self.names = [str(x) for x in names]
        self.expression = expression
        self.state = 0
        self.sequence = []
        self.else_sequence = []

        try:
            self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        except Exception as e:
            raise ParseError.ParseError(expression, "Could not compile Python expression.") from e

    def __repr__(self):
        s = "<for "
        s+= ", ".join(self.names)
        s+= " in %s: %s" % (str(self.expression), repr(self.sequence))
        if self.else_sequence:
            s+= " else %s" % repr(self.else_sequence)
        return s + ">"

    def append(self, node):
        if self.state == 0:
            self.sequence.append(node)
        else:
            self.else_sequence.append(node)

    def appendElse(self):
        if self.state != 0:
            raise ParseError(self.source, "Only one #else allowed on an #if statement.")

        self.state = 1

    def render(self, context):
        try:
            result = context.eval(self.code)
        except Exception as e:
            raise RenderError.RenderError(self.expression, "Could not evaluate Python expression.") from e

        if result:
            if "loop" in context.locals:
                outer = context.locals[loop]
            else:
                outer = None

            for i, values in enumerate(result):
                context["loop"] = ForNode.LoopContext(i, values, len(result), outer)

                if len(self.names) == 1:
                    context[self.names[0]] = values
                else:
                    for name, value in zip(self.names, values):
                        context[name] = value

                r = Node.Node.renderSequence(context, self.sequence)

                # Reset "loop" variable in case we return.  
                if outer is None:
                    del context["loop"]
                else:
                    context["loop"] = outer

                if isinstance(r, ContinueNode.ContinueNode):
                    continue
                elif isinstance(r, BreakNode.BreakNode):
                    break
                elif isinstance(r, ReturnNode.ReturnNode):

                    return r

        else:
            return Node.Node.renderSequence(context, self.else_sequence)

        return None

