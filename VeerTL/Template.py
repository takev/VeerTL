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

from . import Node

class Template (Node.Node):
    def __init__(self, context):
        super().__init__(context)
        self.sequence = []

    def __repr__(self):
        return "[%s]" % (", ".join(repr(x) for x in self.sequence))

    def append(self, node):
        self.sequence.append(node)

    def makeRenderContext(self, _globals={}):
        return self.parse_context.makeRenderContext(_globals=_globals)

    def render(self, context):
        return Node.Node.renderSequence(context, self.sequence)


