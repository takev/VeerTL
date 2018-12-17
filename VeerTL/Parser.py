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

import re
import sys

from . import ParseError
from . import ParseContext

from . import EndToken
from . import DoToken
from . import ElseToken
from . import BreakToken
from . import ContinueToken
from . import ReturnToken
from . import IfToken
from . import ElifToken
from . import WhileToken
from . import IncludeToken
from . import ForToken
from . import FunctionToken
from . import BlockToken
from . import TextToken
from . import PlaceholderToken
from . import StatementToken
from . import FlowControlToken

from . import Template
from . import IfNode
from . import ForNode
from . import DoWhileNode

STATEMENT_PARSERS = {
    "end": EndToken.EndToken,
    "do": DoToken.DoToken,
    "else": ElseToken.ElseToken,
    "break": BreakToken.BreakToken,
    "continue": ContinueToken.ContinueToken,
    "return": ReturnToken.ReturnToken,
    "if": IfToken.IfToken,
    "elif": ElifToken.ElifToken,
    "while": WhileToken.WhileToken,
    "include": IncludeToken.IncludeToken,
    "for": ForToken.ForToken,
    "function": FunctionToken.FunctionToken,
    "block": BlockToken.BlockToken,
}
def parseToken(source, start_char):
    if source.startswith(start_char + "{"):
        return PlaceholderToken.PlaceholderToken(source)

    elif source.startswith(start_char + start_char):
        return StatementToken.StatementToken(source)

    elif source.startswith(start_char):
        token_string = str((source + 1).getSimpleToken())
        try:
            statement_parse_function = STATEMENT_PARSERS[token_string]
        except KeyError:
            return TextToken.TextToken(source[:source.start + 1])

        return statement_parse_function(source)

    else:
        return TextToken.TextToken(source[:source.start + 1])

def tokenize(source, start_char):
    """
    >>> from SourceFile import SourceFile

    >>> list(tokenize(SourceFile("", "foo %{bar} baz")))
    ['foo ', %{bar}, ' baz']

    >>> list(tokenize(SourceFile("", "foo\\n%if zap == 3\\nzip\\n%end\\nbaz")))
    ['foo\\n', <if zap == 3>, 'zip\\n', <end>, 'baz']

    >>> list(tokenize(SourceFile("", "foo\\n%while zap == 3\\nzip\\n%end\\nbaz")))
    ['foo\\n', <while zap == 3>, 'zip\\n', <end>, 'baz']

    >>> list(tokenize(SourceFile("", "foo\\n%for zap in 3 + 5\\nzip\\n%end\\nbaz")))
    ['foo\\n', <for zap in 3 + 5>, 'zip\\n', <end>, 'baz']

    >>> list(tokenize(SourceFile("", "\\tfoo\\r\\n%% a = 5\\r\\nzip\\r\\n%end\\r\\nbaz")))
    ['\\tfoo\\r\\n', <statement 'a = 5\\n'>, 'zip\\r\\n', <end>, 'baz']

    """
    while True:
        i = source.text.find(start_char, source.start)
        if i != -1:
            token = TextToken.TextToken(source[:i])
            if token:
                yield token

            source = token.getRest()

            token = parseToken(source, start_char=start_char)
            yield token
            source = token.getRest()

        else:
            token = TextToken.TextToken(source[:])
            if token:
                yield token

            break

def optimizedTokenize(source, start_char):
    """
    >>> from SourceFile import SourceFile

    >>> list(optimizedTokenize(SourceFile("", "foo $ baz")))
    ['foo $ baz']

    >>> list(optimizedTokenize(SourceFile("", "%% if a == 3:\\n%%     a = 5\\n")))
    [<statement 'if a == 3:\\n    a = 5\\n'>]
    """

    previous_token = None
    for token in tokenize(source, start_char=start_char):

        if not previous_token or not previous_token.merge(token):
            yield token
            previous_token = token

def parse(source, context=ParseContext.ParseContext()):
    """
    >>> from SourceFile import SourceFile
    >>> from RenderContext import RenderContext

    >>> parse(SourceFile("", "foo %{bar} baz"))
    ['foo ', %{bar}, ' baz']

    >>> parse(SourceFile("", "foo\\n%if zap == 3\\nzip\\n%end\\nbaz"))
    ['foo\\n', <if zap == 3: ['zip\\n']>, 'baz']

    >>> parse(SourceFile("", "foo\\n%if zap == 3\\nzip\\n%else\\nbar\\n%end\\nbaz"))
    ['foo\\n', <if zap == 3: ['zip\\n'] else ['bar\\n']>, 'baz']

    >>> parse(SourceFile("", "foo\\n%if zap == 3\\nzip\\n%elif zap > 4\\ntip\\n%else\\nbar\\n%end\\nbaz"))
    ['foo\\n', <if zap == 3: ['zip\\n'] elif zap > 4: ['tip\\n'] else ['bar\\n']>, 'baz']

    >>> parse(SourceFile("", "foo\\n%while zap == 3\\nzip\\n%end\\nbaz"))
    ['foo\\n', <while zap == 3: ['zip\\n']>, 'baz']

    >>> parse(SourceFile("", "foo\\n%do\\nzip\\n%while zap == 3\\nbaz"))
    ['foo\\n', <dowhile zap == 3: ['zip\\n']>, 'baz']

    >>> parse(SourceFile("", "foo\\n%for zap in 3 + 5\\nzip\\n%end\\nbaz"))
    ['foo\\n', <for zap in 3 + 5: ['zip\\n']>, 'baz']

    >>> parse(SourceFile("", "foo\\n%for zap in 3 + 5\\nzip\\n%else\\nbar\\n%end\\nbaz"))
    ['foo\\n', <for zap in 3 + 5: ['zip\\n'] else ['bar\\n']>, 'baz']

    >>> parse(SourceFile("", "foo\\n%function zap(a, b)\\nzip\\n%end\\nbaz"))
    ['foo\\n', <function zap(a, b): ['zip\\n']>, 'baz']

    >>> parse(SourceFile("", "foo\\n%% a = 5\\nbar\\n"))
    ['foo\\n', <statement 'a = 5\\n'>, 'bar\\n']

    >>> template = parse(SourceFile("tests/test.vc"))
    >>> repr(template)
    >>> context = template.makeRenderContext()
    >>> template.render(context)
    >>> str(context)

    """
    token_stack = [Template.Template(context)]
    for token in optimizedTokenize(source, start_char=context.start_char):
        if not token_stack:
            raise ParseError.ParseError(token.source, "Unbalanced, too many, 'end' statement.")

        top = token_stack[-1]

        if isinstance(token, EndToken.EndToken):
            if len(token_stack) < 2:
                raise ParseError.ParseError(token.source, "Unbalanced, too many, 'end' statement.")

            token_stack.pop()

        elif isinstance(token, WhileToken.WhileToken):
            if isinstance(top, DoWhileNode.DoWhileNode):
                top.appendWhile(token.expression)
                token_stack.pop()

            else:
                ast_node = token.getNode(context)
                top.append(ast_node)
                token_stack.append(ast_node)

        elif isinstance(token, FunctionToken.FunctionToken) or isinstance(token, BlockToken.BlockToken):
            if not isinstance(top, Template.Template):
                raise ParseError.ParseError(token.source, "'function' or 'block' may only be instantiated at top level of a file.")

            ast_node = token.getNode(context)
            top.append(ast_node)
            token_stack.append(ast_node)

        elif isinstance(token, FlowControlToken.FlowControlToken):
            ast_node = token.getNode(context)
            top.append(ast_node)
            token_stack.append(ast_node)

        elif isinstance(token, ElifToken.ElifToken):
            if not isinstance(top, IfNode.IfNode):
                raise ParseError.ParseError(token.source, "Unexpected 'elif' statement.")

            top.appendElif(token.expression)

        elif isinstance(token, ElseToken.ElseToken):
            if not isinstance(top, IfNode.IfNode) and not isinstance(top, ForNode.ForNode):
                raise ParseError.ParseError(token.source, "Unexpected 'else' statement.")

            top.appendElse()

        elif isinstance(token, IncludeToken.IncludeToken):
            if not isinstance(top, Template.Template):
                raise ParseError.ParseError(token.source, "'include' can only be instantiated at top level of a file.")

            top.append(token.getNode(context))

        else:
            top.append(token.getNode(context))

    if not token_stack:
        raise ParseError.ParseError(token.source, "Unbalanced, too many, 'end' statement.")
    elif len(token_stack) > 1:
        raise ParseError.ParseError(token.source, "Unbalanced, too few, 'end' statement.")

    template = token_stack[-1]
    return template




if __name__ == "__main__":
    import doctest
    doctest.testmod()
