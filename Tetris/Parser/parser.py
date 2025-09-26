
from Tetris.Ast1.statements import BlockStmt
from Tetris.Lexer.Tokens import TokenKind
from Tetris.Parser.init_lookups import createTokenLookUps
from Tetris.Parser.stmt import parse_stmt


class Parser:

    def __init__(self, tokenarray, pos):
        self.tokens = tokenarray
        self.pos = pos

    def currentToken(self):
        return self.tokens[self.pos]

    def currentTokenKind(self):
        return self.currentToken().tokenKind

    def advance(self):
        tk = self.currentToken()
        self.pos += 1
        return tk

    def hasTokens(self):
        return self.pos < len (self.tokens) and self.currentTokenKind() != TokenKind.IOF

    def expect_error(self, expected_kind, err=None):
        token = self.currentToken()
        kind = token.tokenKind

        if kind != expected_kind:
            if err is None:
                err = f"Expected {expected_kind} but received {kind} instead"
            raise Exception(err)

        return self.advance()

    def expect(self, expected_kind):
        return self.expect_error(expected_kind, None)

def createParser(tokens,pos):
    createTokenLookUps()
    return Parser(tokens,pos)

def parse(tokens):
    body = []
    p = createParser(tokens,0)

    while p.hasTokens():
        body.append(parse_stmt(p))
    return BlockStmt(body)


