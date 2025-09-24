
from Lexer import  tokenize
from Tokens import  debug

file_path = "tetris.brik"


with open(file_path, "r", encoding="utf-8") as file:
    bytes = file.read()


tokens = tokenize(str(bytes))

# Print the tokens
for token in tokens:
    print(debug(token))








