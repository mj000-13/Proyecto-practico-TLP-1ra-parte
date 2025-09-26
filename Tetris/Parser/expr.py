import ast

from Tetris.Ast1.ast import Expr,Stmt
from Tetris.Lexer.Tokens import TokenKind
from Tetris.Ast1.expressions import NumberExpr, StringExpr, SymbolExpr, BinaryExpr
from Tetris.Parser.bindingPowers import BindingPower
from Tetris.Parser.lookups import nud_lu,bp_lu,led_lu


def parse_expr(p, bp):
    token_kind = p.currentTokenKind()
    nud_fn = nud_lu.get(token_kind)

    if nud_fn is None:
        raise Exception(f"NUD Handler expected for token {token_kind}")

    left = nud_fn(p)

    while bp_lu.get(p.currentTokenKind(), BindingPower.default_bp) > bp:
        token_kind = p.currentTokenKind()
        led_fn = led_lu.get(token_kind)

        if led_fn is None:
            raise Exception(f"LED Handler expected for token {token_kind}")

        left = led_fn(p, left, bp)

    return left

def parse_primary_expr(p):
    kind = p.currentTokenKind()

    if kind == TokenKind.NUMBER:
        number = float(p.advance().value)
        return NumberExpr(number)

    elif kind == TokenKind.STRING:
        return StringExpr(p.advance().value)

    elif kind == TokenKind.IDENTIFIER:
        return SymbolExpr(p.advance().value)

    else:
        raise Exception(
            f"Cannot create primary_expr from {p.currentTokenKind()}"
        )

def parse_binary_expression(p, left, bp):
    operatorToken = p.advance()
    right = parse_expr(p, bp_lu[operatorToken.tokenKind])
    return BinaryExpr(left, operatorToken, right)