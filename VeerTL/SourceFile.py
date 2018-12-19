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
import os.path

from . import ParseError

class SourceFile (object):
    BRACKET_REVERSE = str.maketrans("([{}])", ")]}{[(")

    def __init__(self, path, text=None, start=0, stop=None):
        if path == "":
            self.path = "<str>"
        elif path.startswith("<"):
            self.path = path
        else:
            self.path = os.path.abspath(path)

        self.start = start
        if text is None:
            self.text = open(self.path, "rt", encoding="UTF-8").read()
        else:
            self.text = text

        if stop is None:
            self.stop = len(self.text)
        else:
            self.stop = stop

    def __len__(self):
        return self.stop - self.start

    def __add__(self, other):
        if isinstance(other, int):
            return self[self.start + other:]
        else:
            raise ValueError("Only integers can be added to a SourceFile.")

    def __getitem__(self, index):
        """Only absolute slices, compared to the original text can be used.
        """

        if isinstance(index, slice):
            if index.step is not None:
                raise IndexError("SourceFile does not support slicing with step.")

            new_start = self.start if index.start is None else index.start
            new_stop = self.stop if index.stop is None else index.stop

            if new_start > new_stop:
                raise IndexError("SourceFile does not support reverse slicing [%i:%i]." % (new_start, new_stop))

            return SourceFile(path=self.path, text=self.text, start=new_start, stop=new_stop)

        else:
            raise IndexError("SourceFile can not be indiced, only sliced.")

    def includePath(self, relative_path):
        directory = os.path.dirname(self.path)
        return os.path.abspath(os.path.join(directory, relative_path))

    def lineNumber(self):
        return self.text.count("\n", 0, self.start) + 1

    def columnNumber(self):
        try:
            return self.start - self.text.rindex("\n", 0, self.start) + 2
        except ValueError:
            return self.start + 1

    def __repr__(self):
        return "%s:%i:%i" % (os.path.relpath(self.path), self.lineNumber(), self.columnNumber())

    def __str__(self):
        return self.text[self.start:self.stop]

    def isSameFile(self, other):
        if self.path != other.path:
            return False
        if len(self.text) != len(other.text):
            return False
        return hash(self.text) == hash(other.text)

    def merge(self, other):
        """Merge SourceFile if they point to the same file and the stop and start line up.
        """
        if not self.isSameFile(other) or self.stop != other.start:
            return False

        self.stop = other.stop
        return True

    def getRest(self):
        return self[self.stop:len(self.text)]

    def startswith(self, needle):
        return self.text.startswith(needle, self.start, self.stop)

    def expand(self):
        """Expand slice until a whole line, including trailing linefeed, is selected.
        """

        start = self.start
        while start > 0 and self.text[start] in "\r\t ":
            start -= 1

        stop = self.stop
        while stop < len(self.text) and self.text[stop] in "\r\t ":
            stop += 1

        # Absorb trailing line feed.
        if stop < len(self.text) and self.text[stop] == "\n":
            stop += 1

        return self[start:stop]

    def strip(self):
        # Skip whitespace.
        start = self.start
        while start < self.stop and self.text[start].isspace():
            start += 1

        stop = self.stop
        while stop > self.start and self.text[stop-1].isspace():
            stop -= 1
        
        return self[start:stop] 

    def getLine(self):
        try:
            new_stop = self.text.index("\n", self.start, self.stop)
        except ValueError:
            new_stop = self.stop

        return self[:new_stop]

    def getSimpleToken(self):
        # Skip whitespace.
        start = self.start
        while start < self.stop and self.text[start].isspace():
            start += 1

        # Return an string of indentifier characters, or a string of other characters.
        first_isidentifier = self.text[start].isidentifier()
        stop = start
        while stop < self.stop and not self.text[stop].isspace() and self.text[stop].isidentifier() == first_isidentifier:
            stop += 1

        return self[start:stop]

    def getSimpleExpression(self, end_chars="\r\n"):
        start = self.start
        stop = self.start
        bracket_stack = []
        while stop < self.stop and (bracket_stack or self.text[stop] not in end_chars):
            c = self.text[stop]

            top = bracket_stack[-1] if bracket_stack else "~"

            if top == "\\":
                bracket_stack.pop()

            elif top in "'\"":
                # Inside string.
                if c == "\\":
                    bracket_stack.append("\\")

                elif top == c:
                    bracket_stack.pop()

            else:
                if c in "([{'\"":
                    bracket_stack.append(c)

                elif c in ")]}":
                    if top.translate(SourceFile.BRACKET_REVERSE) == c:
                        bracket_stack.pop()
                    else:
                        raise ParseError.ParseError(
                            self[start:stop],
                            "Unexpected end bracket '%c', expected '%c'." % (
                                c,
                                top.translate(SourceFile.BRACKET_REVERSE)
                            )
                        )

            stop += 1

        if bracket_stack:
            raise ParseError(self[start:stop], "Brackets not balanced in expression %s" % bracket_stack)

        return self[start:stop]

