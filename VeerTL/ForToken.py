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
from . import FlowControlToken
from . import ForNode

class ForToken (Token.Token, FlowControlToken.FlowControlToken):
    def __init__(self, token_source):
        source = (token_source + 1).getSimpleToken().getRest()

        self.names = []
        while True:
            name = source.getSimpleToken()
            self.names.append(name)
            source = name.getRest()

            comma = source.getSimpleToken()
            source = comma.getRest()
            if str(comma) == ",":
                continue
            elif str(comma) == "in":
                break
            else:
                raise ParseError(comma, "Unexpected string '%s'." % str(comma))

        self.expression = source.getSimpleExpression().strip()
        super().__init__(token_source[:self.expression.stop])

    def __repr__(self):
        return "<for %s in %s>" % (", ".join(str(x) for x in self.names), str(self.expression))

    def getNode(self, context):
        return ForNode.ForNode(context, self.names, self.expression)

