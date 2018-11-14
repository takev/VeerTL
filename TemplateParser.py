"""Parse a text file as a template.

Placeholders:
    ${ <expr> }

Python execution:
    ## <python line>
    ## <python line>
    ## <python line>

Statements:
    #if <expr>
    #else
    #end

    #for <name(s)> in <expr>
    #break
    #continue
    #end

    #while <expr>
    #end

    #function <name>(<argument(s)>)
    #end

    #block <name>
    #end

    #include <filename>
    #inherint <filename>
"""

import heapq
import re
import os.path

class SourceSlice (object):
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

class Token (object):
    def __init__(self, source):
        self.source = source

    def getRest(self):
        return self.source.getRest()

class SimpleToken (Token):
    def __init__(self, source):
        token_name = (source + 1).getSimpleToken()
        Token.__init__(self, source[:token_name.stop])

    def __repr__(self):
        return "<%s>" % str(self.source + 1)

class SimpleExpressionToken (Token):
    def __init__(self, source, attribute):
        expression = (source + 1).getSimpleToken().getRest().getSimpleExpression()
        setattr(self, attribute, expression)
        Token.__init__(self, source[:expression.stop])

class EndToken (SimpleToken):
    pass

class DoToken (SimpleToken):
    pass

class ElseToken (SimpleToken):
    pass

class BreakToken (SimpleToken):
    pass

class ContinueToken (SimpleToken):
    pass

class TextToken (Token):
    def __repr__(self):
        return repr(str(self.source))

class ReturnToken (SimpleExpressionToken):
    def __init__(self, source):
        SimpleExpressionToken.__init__(self, source, "expression")

    def __repr__(self):
        return "<return %s>" % str(self.expression)

class IfToken (SimpleExpressionToken):
    def __init__(self, source):
        SimpleExpressionToken.__init__(self, source, "expression")

    def __repr__(self):
        return "<if %s>" % str(self.expression)

class ElifToken (SimpleExpressionToken):
    def __init__(self, source):
        SimpleExpressionToken.__init__(self, source, "expression")

    def __repr__(self):
        return "<elif %s>" % str(self.expression)

class WhileToken (SimpleExpressionToken):
    def __init__(self, source):
        SimpleExpressionToken.__init__(self, source, "expression")

    def __repr__(self):
        return "<while %s>" % str(self.expression)

class BlockToken (SimpleExpressionToken):
    def __init__(self, source):
        SimpleExpressionToken.__init__(self, source, "name")

    def __repr__(self):
        return "<block %s>" % str(self.name)

class IncludeToken (SimpleExpressionToken):
    def __init__(self, source):
        SimpleExpressionToken.__init__(self, source, "path")

    def __repr__(self):
        return "<include %s>" % str(self.path)

class InherintToken (SimpleExpressionToken):
    def __init__(self, source):
        SimpleExpressionToken.__init__(self, source, "path")

    def __repr__(self):
        return "<inherint %s>" % str(self.path)

class ForToken (Token):
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

        self.expression = source.getSimpleExpression()
        Token.__init__(self, token_source[:self.expression.stop])

    def __repr__(self):
        return "<for %s in %s>" % (", ".join(str(x) for x in self.names), str(self.expression))

class FunctionToken (Token):
    def __init__(self, token_source):
        source = (token_source + 1).getSimpleToken().getRest()

        self.name = source.getSimpleToken()
        source = self.name.getRest()

        open_bracket = source.getSimpleToken()
        source = open_bracket.getRest()
        if str(open_bracket) != "(":
            raise ParseError(open_bracket, "Expecting open bracket '(', but got '%s'." % str(open_bracket))

        self.arguments = []
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
                raise ParseError(comma, "Unexpected string '%s'." % str(comma))

        Token.__init__(self, token_source[:comma.stop])

    def __repr__(self):
        return "<function %s(%s)>" % (self.name, ", ".join(str(x) for x in self.names))

class PlaceholderToken (Token):
    def __init__(self, source):
        self.expression = (source + 2).getSimpleExpression("}")
        Token.__init__(self, source[:self.expression.stop + 1])

    def __repr__(self):
        return "${" + str(self.expression) + "}"

class StatementToken (Token):
    def __init__(self, source):
        self.statement = (source + 2).getSimpleExpression()
        Token.__init__(self, source[:self.statement.stop])

    def __repr__(self):
        return "<statement %s>" % str(self.statement)

STATEMENT_PARSERS = {
    "end": EndToken,
    "do": DoToken,
    "else": ElseToken,
    "break": BreakToken,
    "continue": ContinueToken,
    "return": ReturnToken,
    "if": IfToken,
    "elif": ElifToken,
    "while": WhileToken,
    "block": BlockToken,
    "include": IncludeToken,
    "inherint": InherintToken,
    "for": ForToken,
    "function": FunctionToken,
}
def parseToken(source):
    if source.startswith("${"):
        return PlaceholderToken(source)

    elif source.startswith("##"):
        return StatementToken(source)

    elif source.startswith("#"):
        token_string = str((source + 1).getSimpleToken())
        try:
            statement_parse_function = STATEMENT_PARSERS[token_string]
        except KeyError:
            return Text(source[:source.start + 1])

        return statement_parse_function(source)

    else:
        return TextToken(source[:source.start + 1])

START_TOKEN_RE = re.compile("[$#]")
def tokenize(source):
    """
    >>> list(tokenize(SourceSlice("", "foo ${bar} baz")))
    ['foo ', ${bar}, ' baz']

    >>> list(tokenize(SourceSlice("", "foo\\n#if zap == 3\\nzip\\n#end\\nbaz")))
    ['foo\\n', <if zap == 3>, '\\nzip\\n', <end>, '\\nbaz']

    >>> list(tokenize(SourceSlice("", "foo\\n#while zap == 3\\nzip\\n#end\\nbaz")))
    ['foo\\n', <while zap == 3>, '\\nzip\\n', <end>, '\\nbaz']

    >>> list(tokenize(SourceSlice("", "foo\\n#for zap in 3 + 5\\nzip\\n#end\\nbaz")))
    ['foo\\n', <for zap in 3 + 5>, '\\nzip\\n', <end>, '\\nbaz']

    >>> list(tokenize(SourceSlice("", "\\tfoo\\r\\n## a = 5\\r\\nzip\\r\\n#end\\r\\nbaz")))
    ['\\tfoo\\r\\n', <statement a = 5>, '\\r\\nzip\\r\\n', <end>, '\\r\\nbaz']

    """
    while True:
        match = START_TOKEN_RE.search(source.text, source.start)
        if match:
            token = TextToken(source[:match.start(0)])
            yield token
            source = token.getRest()

            token = parseToken(source)
            yield token
            source = token.getRest()

        else:
            yield TextToken(source[:])
            break

class NoReturn:
    pass

class ASTNode (object):
    def __init__(self):
        pass

    @classmethod
    def renderSequence(cls, output, namespace, sequence):
        for node in self.sequence:
            r = node.render(self, output, namespace)
            if not isinstance(NoReturn):
                return r
        return r

class Template (ASTNode):
    def __init__(self):
        self.sequence = []

    def append(self, node):
        self.sequence.append(node)

    def render(self, output, namespace):
        return ASTNode.renderSequence(output, namespace, self.sequence)

class TextAST (ASTNode):
    def __init__(self, text):
        self.text = text
        self.code = str(text)

    def render(self, output, namespace):
        output.append(self.code)
        return NoReturn()

class BreakAST (ASTNode):
    def __init__(self, source):
        self.source = source

    def render(self, output, namespace):
        return self

class ContinueAST (ASTNode):
    def __init__(self, source):
        self.source = source

    def render(self, output, namespace):
        return self

class ReturnAST (ASTNode):
    def __init__(self, expression):
        self.expression = expression
        self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")

    def render(self, output, namespace):
        try:
            result = eval(self.code, {}, namespace)
        except Exception, e:
            raise RenderError(self.expression, e)

        return result

class PlaceholderAST (ASTNode):
    def __init__(self, expression):
        self.expression = expression
        self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")

    def render(self, output, namespace):
        try:
            result = eval(self.code, {}, namespace)
        except Exception, e:
            raise RenderError(self.expression, e)

        output.append(result)
        return NoReturn()

class ForAST (ASTNode):
    def __init__(self, names, expression):
        self.names = [str(x) for x in names]
        self.expression = expression
        self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        self.state = 0
        self.sequence = []
        self.else_sequence = []

    def append(self, node):
        if self.state == 0:
            self.sequence.append(node)
        else:
            self.else_sequence.append(node)

    def appendElse(self):
        if self.state != 0:
            raise ParseError(self.source, "Only one #else allowed on an #if statement.")

        self.state = 1

    def render(self, output, namespace):
        try:
            result = eval(self.code, {}, namespace)
        except Exception, e:
            raise RenderError(self.expression, e)

        if result:
            for i, values in enumerate(result):
                namespace["_first"] = (i == 0)
                namespace["_last"] = (i == (len(result) - 1))

                if len(self.names) == 1:
                    namespace[self.names[0]] = values
                else:
                    for name, value in zip(self.names, values):
                        namespace[name] = value

                r = ASTNode.renderSequence(output, namespace, self.sequence)
                if isinstance(r, ContinueAST):
                    continue
                elif isinstance(r, BreakAST):
                    break
                else:
                    return r

        else:
            return ASTNode.renderSequence(output, namespace, self.else_sequence)

        return NoReturn()

class WhileAST (ASTNode):
    def __init__(self, expression):
        self.expression = expression
        self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")
        self.sequence = []

    def append(self, node):
        self.sequence.append(node)

    def render(self, output, namespace):
        while True:
            try:
                result = eval(self.code, {}, namespace)
            except Exception, e:
                raise RenderError(self.expression, e)

            if not result:
                break

            r = ASTNode.renderSequence(output, namespace, self.sequence)
            if isinstance(r, ContinueAST):
                continue
            elif isinstance(r, BreakAST):
                break
            else:
                return r

        return NoReturn()
        
class DoAST (ASTNode):
    def __init__(self):
        self.sequence = []

    def append(self, node):
        self.sequence.append(node)

    def appendWhile(self, expression)
        self.expression = expression
        self.code = parser.expr(str(expression)).compile("<" + repr(expression) + ">")

    def render(self, output, namespace):
        while True:
            r = ASTNode.renderSequence(output, namespace, self.sequence)
            if isinstance(r, ContinueAST):
                continue
            elif isinstance(r, BreakAST):
                break
            else:
                return r

            try:
                result = eval(self.code, {}, namespace)
            except Exception, e:
                raise RenderError(self.expression, e)

            if not result:
                break

        return NoReturn()
        
class IfAST (ASTNode):
    def __init__(self, expression):
        self.state = 0
        self.expression_sequence = [(
            expression,
            parser.expr(str(expression)).compile("<" + repr(expression) + ">")
            []
        )]
        self.else_sequence = []

    def append(self, node):
        if self.state == 0:
            sequence = self.expression_sequence[-1][1]
            sequence.append(node)
        else:
            self.else_sequence.append(node)

    def appendElif(self, expression):
        self.expression_sequence.append((
            expression,
            parser.expr(str(expression)).compile("<" + repr(expression) + ">")
            []
        ))

    def appendElse(self):
        if self.state != 0:
            raise ParseError(self.source, "Only one #else allowed on an #if statement.")

        self.state = 1

    def render(self, output, namespace):
        for expression, code, sequence in self.expression_sequence:
            try:
                result = eval(code, {}, namespace)
            except Exception, e:
                raise RenderError(expression, e)

            if result:
                return ASTNode.renderSequence(output, namespace, sequence)
        else:
            return ASTNode.renderSequence(output, namespace, self.else_sequence)

class StatementAST (ASTNode):
    def __init__(self, statement):
        self.statement = statement
        self.code = parser.expr(str(statement)).compile("<" + repr(statement) + ">")

    def render(self, output, namespace):
        try:
            exec(self.code, {}, namespace)
        except Exception, e:
            raise RenderError(expression, e)

        return NoReturn()

def parse(source):
    token_stack = [Template()]
    for token in tokenize(source):
        if not token_stack:
            raise ParseError(token.source, "Unbalanced, too many, #end statement.")

        top = token_stack[-1]

        if isinstance(token, TextToken):
            if isinstance(top, TextToken):
                top.mergeText(token.source)
            else:
                top.append(token.getASTNode())

        elif isinstance(token, EndToken):
            if len(token_stack) < 2:
                raise ParseError(token.source, "Unbalanced, too many, #end statement.")

            token_stack.pop()

        elif isinstance(token, WhileToken):
            if isinstance(top, DoToken):
                top.appendWhile(token.expression)
                token_stack.pop()

            else:
                ast_node = token.getASTNode()
                top.append(ast_node)
                token_stack.append(ast_node)

        elif token.__class__.__name__ in ("IfToken", "DoToken", "ForToken", "FunctionToken", "BlockToken"):
            ast_node = token.getASTNode()
            top.append(ast_node)
            token_stack.append(ast_node)

        elif isinstance(token, ElifToken):
            if not isinstance(top, IfAST):
                raise ParseError(token.source, "Unexpected #elif statement.")

            top.appendElif(token.expression)

        elif isinstance(token, ElseToken):
            if not isinstance(top, IfAST) and not isinstance(top, ForAST):
                raise ParseError(token.source, "Unexpected #else statement.")

            top.appendElse()

        else:
            top.append(token.getASTNode())

    if not token_stack:
        raise ParseError(token.source, "Unbalanced, too many, #end statement.")
    elif len(token_stack) > 1:
        raise ParseError(token.source, "Unbalanced, too few, #end statement.")

    return token_stack[-1]




if __name__ == "__main__":
    import doctest
    doctest.testmod()
