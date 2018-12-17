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

class Token (object):
    def __init__(self, source):
        from . import PlaceholderToken
        from . import TextToken
        if isinstance(self, PlaceholderToken.PlaceholderToken) or isinstance(self, TextToken.TextToken):
            self.source = source
        else:
            self.source = source.expand()

    def getRest(self):
        return self.source.getRest()

    def merge(self, other):
        return False
