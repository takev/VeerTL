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
from . import BlockNode

class BlockToken (Token.Token):
    def __init__(self, token_source):
        source = (token_source + 1).getSimpleToken().getRest()
        self.name = source.getSimpleToken()

        super().__init__(token_source[:self.name.stop])

    def __repr__(self):
        return "<block %s>" % (self.name)

    def getNode(self, context):
        return BlockNode.BlockNode(context, self.name)

