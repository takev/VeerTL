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
import parser

from . import FunctionNode
from . import ParseError

class BlockNode (FunctionNode.FunctionNode):
    def __init__(self, context, name):
        super().__init__(context, name, [])

        expression = "%s()" % str(name)
        try:
            self.code = parser.expr(expression).compile("<" + expression + ">")
        except Exception as e:
            raise ParseError.ParseError(expression, "Could not compile Python expression.") from e


    def render(self, context):
        if context.callingBlock(str(self.name)):
            try:
                result = context.eval(self.code)
            except Exception as e:
                raise RenderError.RenderError(self.expression, "Could not evaluate Python expression.") from e

            context.append(result)

        return None

