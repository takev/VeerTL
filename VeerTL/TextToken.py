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

from . import Token
from . import TextNode

class TextToken (Token.Token):
    def __repr__(self):
        return repr(str(self.source))

    def __len__(self):
        return len(self.source)

    def __bool__(self):
        return len(self) > 0

    def getNode(self, context):
        return TextNode.TextNode(context, self.source)

    def merge(self, other):
        if isinstance(other, TextToken):
            return self.source.merge(other.source)
        else:
            return False

