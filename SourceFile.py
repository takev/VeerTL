
class SourceFile (object):
    def __init__(self, path, text=None, start=0, stop=None):
        self.path = path
        self.start = start
        if text is None:
            self.text = open(self.path, "rt", encoding="UTF-8").read()
        else:
            self.text = text

        if stop is None:
            self.stop = len(self.text)
        else:
            self.stop = stop

    def __add__(self, other):
        if isinstance(other, int):
            return self[self.start + other:]
        else:
            raise ValueError("Only integers can be added to a SourceSlice.")

    def __getitem__(self, index):
        """Only absolute slices, compared to the original text can be used.
        """

        if isinstance(index, slice):
            if index.step is not None:
                raise IndexError("SourceSlice does not support slicing with step.")

            new_start = self.start if index.start is None else index.start
            new_stop = self.stop if index.stop is None else index.stop

            if new_start > new_stop:
                raise IndexError("SourceSlice does not support reverse slicing [%i:%i]." % (new_start, new_stop))

            return SourceSlice(path=self.path, text=self.text, start=new_start, stop=new_stop)

        else:
            raise IndexError("SourceSlice can not be indiced, only sliced.")

    def lineNumber(self):
        return self.text.count("\n", 0, self.start) + 1

    def columnNumber(self):
        try:
            return self.text.rindex("\n", 0, self.start) + self.start + 2
        except ValueError:
            return self.start + 1

    def filename(self):
        return os.path.basename(self.path)

    def __repr__(self):
        return "%s:%i:%i" % (self.filename(), self.lineNumber(), self.columnNumber())

    def __str__(self):
        return self.text[self.start:self.stop]

    def getRest(self):
        return self[self.stop:len(self.text)]

    def startswith(self, needle):
        return self.text.startswith(needle, self.start, self.stop)

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
        # Skip whitespace.
        start = self.start
        while start < self.stop and self.text[start].isspace():
            start += 1

        stop = start
        bracket_stack = []
        while stop < self.stop and (bracket_stack or self.text[stop] not in end_chars):
            c = self.text[stop]

            if bracket_stack and bracket_stack[-1] in "\\":
                bracket_stack.pop()

            elif bracket_stack and bracket_stack[-1] in "'\"":
                # Inside string.
                if c == "\\":
                    bracket_stack.append("\\")

                elif c == bracket_stack[-1]:
                    bracket_stack.pop()

            else:
                if c in "([{'\"":
                    bracket_stack.append(c)

                elif c in ")]}":
                    if bracket_stack and bracket_stack[-1] == c:
                        bracket_stack.pop()
                    else:
                        raise ParseError(self[start:stop], "Expected end bracket '%c' in expression." % c)

            stop += 1

        if bracket_stack:
            raise ParseError(self[start:stop], "Brackets not balanced in expression %s" % bracket_stack)

        return self[start:stop]

