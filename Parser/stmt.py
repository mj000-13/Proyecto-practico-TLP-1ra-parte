from Ast1.statements import ExpressionStmt, ClassStatement, ReturnStatement, FunctionStatement
from Ast1.statements import VarDeclStmt
from Parser.expr import parse_expr
from Parser.lookups import stmt_lu, BindingPower
from Lexer.Tokens import TokenKind


def parse_stmt(p):
    token_kind = p.currentTokenKind()
    stmt_fn = stmt_lu.get(token_kind)

    if stmt_fn is not None :
        return stmt_fn(p)
    expression = parse_expr(p,BindingPower.default_bp)
    p.expect(TokenKind.SEMICOMMA)
    return ExpressionStmt(expression)

def parse_var_dcl_stmt(p):
    isconstant = p.advance().tokenKind == TokenKind.CONST
    varname = p.expectError(TokenKind.IDENTIFIER, "Variable declaration empty, expected to find an assignment").value
    p.expect(TokenKind.ASSIGNMENT)
    assignedvalue = parse_expr(p, BindingPower.assignment)
    p.expect(TokenKind.SEMICOMMA)
    return VarDeclStmt(varname, isconstant, assignedvalue)

def parse_return_stmt(p):
    p.expect(TokenKind.RETURN)
    if p.currentTokenKind() not in (TokenKind.SEMICOMMA, TokenKind.CLOSED_CURL):
        value = parse_expr(p, BindingPower.default_bp)
    else:
        value = None
    if p.currentTokenKind() == TokenKind.SEMICOMMA:
        p.advance()
    return ReturnStatement(value)

def parse_function_stmt(p):
    p.expect(TokenKind.DEF)

    name = p.expectError(TokenKind.IDENTIFIER, "Expected function name").value


    p.expect(TokenKind.OPEN_PARENT)
    params = []
    if p.currentTokenKind() != TokenKind.CLOSED_PARENT:
        while True:
            params.append(p.expectError(TokenKind.IDENTIFIER, "Expected parameter name").value)
            if p.currentTokenKind() != TokenKind.COMMA:
                break
            p.advance()
    p.expect(TokenKind.CLOSED_PARENT)

    p.expect(TokenKind.OPEN_CURL)
    body = []
    while p.currentTokenKind() != TokenKind.CLOSED_CURL:
        if p.currentTokenKind() == TokenKind.RETURN:
            body.append(parse_return_stmt(p))
        else:
            body.append(parse_stmt(p))  # cualquier otro statement que tengas
    p.expect(TokenKind.CLOSED_CURL)

    return FunctionStatement(name, params, body)




def parse_class_dcl_stmt(p):
    p.expect(TokenKind.CLASS)
    class_name = p.expectError(TokenKind.IDENTIFIER, "Expected class name").value
    p.expect(TokenKind.OPEN_CURL)

    attributes = []
    methods = []

    while p.currentTokenKind() != TokenKind.CLOSED_CURL:
        if p.currentTokenKind() in (TokenKind.LET, TokenKind.CONST):
            attr = parse_var_dcl_stmt(p)
            attributes.append(attr)
        elif p.currentTokenKind() == TokenKind.DEF:
            method = parse_function_stmt(p)
            methods.append(method)
        else:
            raise SyntaxError(f"Unexpected token in class body: {p.currentToken()}")

    p.expect(TokenKind.CLOSED_CURL)
    return ClassStatement(class_name, attributes, methods)


