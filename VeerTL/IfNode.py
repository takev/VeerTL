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

class IfNode (Node.Node):
    class Branch (object):
        def __init__(self, expression):
            self.expression = expression
            try:
                self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">"),
            except Exception as e:
                raise ParseError.ParseError(expression, "Could not compile Python expression.") from e

            self.sequence = []

        def append(self, node):
            self.sequence.append(node)

    def __init__(self, context, expression):
        super().__init__(context)
        self.state = 0
        self.branches = [IfNode.Branch(expression)]
        self.else_sequence = []

    def __repr__(self):
        s = "<"

        for i, branch in enumerate(self.branches):
            if i == 0:
                s += "if %s: %s" % (str(branch.expression), repr(branch.sequence))
            else:
                s += " elif %s: %s" % (str(branch.expression), repr(branch.sequence))

        if self.else_sequence:
                s += " else %s" % repr(self.else_sequence)

        return s + ">"

    def append(self, node):
        if self.state == 0:
            self.branches[-1].append(node)
        else:
            self.else_sequence.append(node)

    def appendElif(self, expression):
        self.branches.append(IfNode.Branch(expression))

    def appendElse(self):
        if self.state != 0:
            raise ParseError(self.source, "Only one #else allowed on an #if statement.")

        self.state = 1

    def render(self, context):
        for branch in self.branches:
            try:
                result = context.eval(branch.code)
            except Exception as e:
                raise RenderError.RenderError(expression, "Could not evaluate Python expression.") from e

            if result:
                return Node.Node.renderSequence(context, branch.sequence)
        else:
            return Node.Node.renderSequence(context, self.else_sequence)

