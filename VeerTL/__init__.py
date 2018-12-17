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

"""Parse a text file as a template.

Placeholders:
    ${ <expr> }

Python execution:
    ## <python line>
    ## <python line>
    ## <python line>

Statements:
    #if <expr>
    #elif <expr>
    #else
    #end

    #for <name(s)> in <expr>
    #break
    #continue
    #end

    #while <expr>
    #end

    #function <name>(<argument(s)>)
    #return <expr>
    #end

    #include <filename>
"""

