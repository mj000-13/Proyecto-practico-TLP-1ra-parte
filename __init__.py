from Ast1.printast import print_ast
from Lexer.Lexer import tokenize
from Parser import parser




file_path = "Tetris/tetris.brik"

with open(file_path, "r", encoding="utf-8") as file:
    source_code = file.read()

tokens = tokenize(source_code)
ast_tree = parser.parse(tokens)

output_path = "Tetris/ast_output.ast"

with open(output_path, "w", encoding="utf-8") as f:
    print_ast(ast_tree, f)


################

file_path2 = "Snake/Snake2.brik"

with open(file_path2, "r", encoding="utf-8") as file:
    source_code2 = file.read()

tokens2= tokenize(source_code2)
ast_tree2 = parser.parse(tokens2)

output_path2 = "Snake/arbol_snake.ast"

with open(output_path2, "w", encoding="utf-8") as f:
    print_ast(ast_tree2, f)