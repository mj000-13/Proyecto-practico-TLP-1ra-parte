import Tokens
import re

#def regexHandler(lex, reg): # La función toma un lex de tipo lexer, y reg, que es de tipo re.compile()


import re

"""CLASSES"""

class RegexPattern:
    def __init__(self, regex, handler):
        self.regex = regex
        self.handler = handler

""" The Lexer object consists on 5 attributes.
pos = Position
line = 
source = The source code
tokens = An array of token type objects
patterns = An array of regex type handlers patterns."""

class Lexer:
    def __init__(self, source):
        self.pos = 0
        self.line = 1
        self.source = source
        self.Tokens = []
        self.patterns = [
            RegexPattern(re.compile(r"\s+"), skipHandler),
            RegexPattern(re.compile(r"//.*"), commentHandler),
            RegexPattern(re.compile(r'"[^"]*"'), stringHandler),
            RegexPattern(re.compile(r"[0-9]+(\.[0-9]+)?"), numberHandler),
            RegexPattern(re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*"), symbolHandler),
            RegexPattern(re.compile(r"\["), defaultHandler(Tokens.TokenKind.OPEN_BRAC, "[")),
            RegexPattern(re.compile(r"\]"), defaultHandler(Tokens.TokenKind.CLOSED_BRAC, "]")),
            RegexPattern(re.compile(r"\{"), defaultHandler(Tokens.TokenKind.OPEN_CURL, "{")),
            RegexPattern(re.compile(r"\}"), defaultHandler(Tokens.TokenKind.CLOSED_CURL, "}")),
            RegexPattern(re.compile(r"\("), defaultHandler(Tokens.TokenKind.OPEN_PARENT, "(")),
            RegexPattern(re.compile(r"\)"), defaultHandler(Tokens.TokenKind.CLOSED_PARENT, ")")),
            RegexPattern(re.compile(r"=="), defaultHandler(Tokens.TokenKind.EQUAL, "==")),
            RegexPattern(re.compile(r"!="), defaultHandler(Tokens.TokenKind.NOT_EQUAL, "!=")),
            RegexPattern(re.compile(r"="), defaultHandler(Tokens.TokenKind.ASSINGMENT, "=")),
            RegexPattern(re.compile(r"!"), defaultHandler(Tokens.TokenKind.NOT, "!")),
            RegexPattern(re.compile(r"<="), defaultHandler(Tokens.TokenKind.LESS_EQUAL, "<=")),
            RegexPattern(re.compile(r"<"), defaultHandler(Tokens.TokenKind.LESS, "<")),
            RegexPattern(re.compile(r">="), defaultHandler(Tokens.TokenKind.GREATER_EQUAL, ">=")),
            RegexPattern(re.compile(r">"), defaultHandler(Tokens.TokenKind.GREATER, ">")),
            RegexPattern(re.compile(r"\|\|"), defaultHandler(Tokens.TokenKind.OR, "||")),
            RegexPattern(re.compile(r"&&"), defaultHandler(Tokens.TokenKind.AND, "&&")),
            RegexPattern(re.compile(r"\.\."), defaultHandler(Tokens.TokenKind.DOT, "..")),
            RegexPattern(re.compile(r"\."), defaultHandler(Tokens.TokenKind.DOT, ".")),
            RegexPattern(re.compile(r";"), defaultHandler(Tokens.TokenKind.SEMICOMMA, ";")),
            RegexPattern(re.compile(r":"), defaultHandler(Tokens.TokenKind.COLON, ":")),
            RegexPattern(re.compile(r"\?"), defaultHandler(Tokens.TokenKind.QUESTION, "?")),
            RegexPattern(re.compile(r","), defaultHandler(Tokens.TokenKind.COMMA, ",")),
            RegexPattern(re.compile(r"\+\+"), defaultHandler(Tokens.TokenKind.PLUS_PLUS, "++")),
            RegexPattern(re.compile(r"--"), defaultHandler(Tokens.TokenKind.MINUS_MINUS, "--")),
            RegexPattern(re.compile(r"\+="), defaultHandler(Tokens.TokenKind.PLUS_EQUAL, "+=")),
            RegexPattern(re.compile(r"-="), defaultHandler(Tokens.TokenKind.MINUS_EQUAL, "-=")),
            RegexPattern(re.compile(r"\+"), defaultHandler(Tokens.TokenKind.PLUS, "+")),
            RegexPattern(re.compile(r"-"), defaultHandler(Tokens.TokenKind.DASH, "-")),
            RegexPattern(re.compile(r"/"), defaultHandler(Tokens.TokenKind.SLASH, "/")),
            RegexPattern(re.compile(r"\*"), defaultHandler(Tokens.TokenKind.STAR, "*")),
            RegexPattern(re.compile(r"%"), defaultHandler(Tokens.TokenKind.PERCENT, "%")),
        ]

    def advanceN(self, n):
        self.pos += n

    def at(self):
        return self.source[self.pos]

    def advance(self):
        self.pos += 1

    def remainder(self):
        return self.source[self.pos:]

    def push(self, token):
        self.Tokens.append(token)

    def at_eof(self):
        return self.pos >= len(self.source)

"""----------------------------------------------------------------------------"""

"""GLOBAL FUNCTIONS"""
"""Tokenizer: """
#Creates a Lexer Object
def tokenize(source):
    lex = Lexer(source)

    while not lex.at_eof():
        matched = False
        for pattern in lex.patterns:
            loc = pattern.regex.match(lex.remainder())
            if loc is not None and loc.start() == 0:
                pattern.handler(lex, pattern.regex)
                matched = True
                break

        if not matched:
            raise Exception(f"lexer error: unrecognized token near {lex.remainder()}")

    lex.push(Tokens.newToken(Tokens.TokenKind.IOF, "EOF"))
    return lex.Tokens

"""----------------------------------------------------------------------------"""
"""Handlers"""

def defaultHandler(kind, value):
    def handler(lex, _regex):
        lex.advanceN(len(value))
        lex.push(Tokens.newToken(kind, value))
    return handler

def stringHandler(lex, regex):
    match = regex.match(lex.remainder())
    stringLiteral = lex.remainder()[match.start():match.end()]
    lex.push(Tokens.newToken(Tokens.TokenKind.STRING, stringLiteral))
    lex.advanceN(len(stringLiteral))

def numberHandler(lex, regex):
    match = regex.match(lex.remainder())
    num = match.group(0)
    lex.push(Tokens.newToken(Tokens.TokenKind.NUMBER, num))
    lex.advanceN(len(num))


def symbolHandler(lex, regex):
    match = regex.match(lex.remainder())
    if not match:
        return

    sym = match.group(0)  # Obtener la cadena

    # Acceder al diccionario dentro de TokenKind
    kind = Tokens.reserved_lu.get(sym.lower(), Tokens.TokenKind.IDENTIFIER)

    lex.push(Tokens.newToken(kind, sym))
    lex.advanceN(len(sym))
    


def skipHandler(lex, regex):
    match = regex.match(lex.remainder())
    lex.advanceN(match.end())

def commentHandler(lex, regex):
    match = regex.match(lex.remainder())
    if match is not None:
        lex.advanceN(match.end())
        lex.line += 1







