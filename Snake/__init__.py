from Ast1.printast import print_ast
from Lexer.Lexer import tokenize
from Parser import parser




file_path = "Snake2.brik"

with open(file_path, "r", encoding="utf-8") as file:
    source_code = file.read()

tokens = tokenize(source_code)
ast_tree = parser.parse(tokens)

output_path = "Snake/arbol_snake.ast"

with open(output_path, "w", encoding="utf-8") as f:
    print_ast(ast_tree, f)