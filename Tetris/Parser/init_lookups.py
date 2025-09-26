from Tetris.Parser.lookups import led,nud, stmt
from Tetris.Parser.bindingPowers import BindingPower
from Tetris.Lexer.Tokens import TokenKind
from Tetris.Parser.expr import parse_primary_expr,parse_binary_expression

def createTokenLookUps():

    #Binary Expressions

    #Logical
    led(TokenKind.AND,BindingPower.logical ,parse_binary_expression)
    led(TokenKind.OR,BindingPower.logical, parse_binary_expression)

    #Relational
    led(TokenKind.LESS,BindingPower.relational, parse_binary_expression)
    led(TokenKind.LESS_EQUAL,BindingPower.relational, parse_binary_expression)
    led(TokenKind.GREATER,BindingPower.relational,parse_binary_expression)
    led(TokenKind.GREATER_EQUAL,BindingPower.relational, parse_binary_expression)
    led(TokenKind.EQUAL, BindingPower.relational,parse_binary_expression)
    led(TokenKind.NOT_EQUAL,BindingPower.relational, parse_binary_expression)

    #Additive and mulplicative
    led(TokenKind.PLUS, BindingPower.additive, parse_binary_expression)
    led(TokenKind.DASH, BindingPower.additive, parse_binary_expression)
    led(TokenKind.STAR, BindingPower.multiplicative, parse_binary_expression)
    led(TokenKind.SLASH, BindingPower.multiplicative,parse_binary_expression)
    led(TokenKind.PERCENT, BindingPower.multiplicative, parse_binary_expression)



    #Primary Expressions
    nud(TokenKind.NUMBER,BindingPower.primary , parse_primary_expr)
    nud(TokenKind.STRING,BindingPower.primary, parse_primary_expr)
    nud(TokenKind.IDENTIFIER,BindingPower.primary ,parse_primary_expr)