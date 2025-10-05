
from Lexer.Tokens import TokenKind
from Ast1.expressions import NumberExpr, StringExpr, SymbolExpr, BinaryExpr, PrefixExpr, AssignmentExpr, \
    ArrayExpr
from Parser.bindingPowers import BindingPower
from Parser.lookups import nud_lu,bp_lu,led_lu


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

        left = led_fn(p, left, bp_lu[p.currentTokenKind()])

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

def parse_assignment_expr(p, left, bp):
    operatorToken = p.advance()
    rhs = parse_expr(p, bp)
    return AssignmentExpr(left,operatorToken ,rhs)


def parse_prefix_expr(p):
    operatorToken = p.advance()
    rhs = parse_expr(p, BindingPower.default_bp)

    return PrefixExpr(operatorToken, rhs)

def parse_grouping_expr(p):
    p.advance()
    expr = parse_expr(p,BindingPower.default_bp)
    p.expect(TokenKind.CLOSED_PARENT)
    return expr

def parse_array_expr(p):
    p.expect(TokenKind.OPEN_BRAC)
    elements = []
    if p.currentTokenKind() != TokenKind.CLOSED_BRAC:
        while True:
            elements.append(parse_expr(p, BindingPower.default_bp))
            if p.currentTokenKind() == TokenKind.CLOSED_BRAC:
                break
            p.expect(TokenKind.COMMA)
    p.expect(TokenKind.CLOSED_BRAC)
    return ArrayExpr(elements)