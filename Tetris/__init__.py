from Tetris.Lexer.Lexer import tokenize
from Tetris.Lexer.Tokens import debug
from Tetris.Parser import parser
from Tetris.Ast1.printast import print_ast



file_path = "tetris.brik"

with open(file_path, "r", encoding="utf-8") as file:
    source_code = file.read()

tokens = tokenize(source_code)
ast_tree = parser.parse(tokens)


with open("ast_output.brik", "w", encoding="utf-8") as f:
    print_ast(ast_tree, f)