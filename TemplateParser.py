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
