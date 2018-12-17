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

from . import ParseError
from . import Token
from . import FunctionNode

class FunctionToken (Token.Token):
    def __init__(self, token_source):
        source = (token_source + 1).getSimpleToken().getRest()

        self.arguments = []
        self.name = source.getSimpleToken()
        source = self.name.getRest()

        open_bracket = source.getSimpleToken()
        source = open_bracket.getRest()
        if str(open_bracket) == "(":
            while True:
                name = source.getSimpleToken()
                if str(name) == ")":
                    break

                self.arguments.append(name)
                source = name.getRest()

                comma = source.getSimpleToken()
                source = comma.getRest()
                if str(comma) == ",":
                    continue
                elif str(comma) == ")":
                    break
                else:
                    raise ParseError.ParseError(comma, "Unexpected string '%s'." % str(comma))

            super().__init__(token_source[:comma.stop])

        elif str(open_bracket) == "()":
            super().__init__(token_source[:open_bracket.stop])

        else:
            raise ParseError.ParseError(open_bracket, "Expecting open bracket '(', but got '%s'." % str(open_bracket))


    def __repr__(self):
        return "<function %s(%s)>" % (self.name, ", ".join(str(x) for x in self.names))

    def getNode(self, context):
        return FunctionNode.FunctionNode(context, self.name, self.arguments)

