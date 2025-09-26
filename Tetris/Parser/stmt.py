from Tetris.Ast1.statements import ExpressionStmt
from Tetris.Parser.expr import parse_expr
from Tetris.Parser.lookups import stmt_lu, BindingPower
from Tetris.Lexer.Tokens import TokenKind


def parse_stmt(p):
    token_kind = p.currentTokenKind()
    stmt_fn = stmt_lu.get(token_kind)

    if stmt_fn is not None :
        return stmt_fn(p)
    expression = parse_expr(p,BindingPower.default_bp)
    p.expect(TokenKind.SEMICOMMA)
    return ExpressionStmt(expression)