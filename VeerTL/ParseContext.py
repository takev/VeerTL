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

from . import ParseError
from . import RenderContext

class ParseContext (object):
    def __init__(self):
        self.start_char = "%"
        self.functions = {}

    def addFunction(self, name, func):
        old_func = self.functions.get(str(name), None)
        self.functions[str(name)] = func
        return old_func

    def makeRenderContext(self):
        _globals = self.functions.copy()
        return RenderContext.RenderContext(_globals=_globals, _locals=_globals)

