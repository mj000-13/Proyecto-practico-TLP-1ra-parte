from Tetris.Lexer.Tokens import Token

def print_ast(node, file, indent=0):

    spacing = '  ' * indent

    if hasattr(node, 'body'):  # BlockStmt
        file.write(f"{spacing}BlockStmt\n")
        file.write(f"{spacing}  body:\n")
        for stmt in node.body:
            print_ast(stmt, file, indent + 2)

    elif hasattr(node, 'expression'):  # ExpressionStmt
        file.write(f"{spacing}ExpressionStmt\n")
        file.write(f"{spacing}  expression:\n")
        print_ast(node.expression, file, indent + 2)

    elif hasattr(node, 'operator') and hasattr(node, 'left') and hasattr(node, 'right'):  # BinaryExpr
        file.write(f"{spacing}BinaryExpr(operator={node.operator.lexeme})\n")
        file.write(f"{spacing}  left:\n")
        print_ast(node.left, file, indent + 2)
        file.write(f"{spacing}  right:\n")
        print_ast(node.right, file, indent + 2)

    elif hasattr(node, 'value'):  # NumberExpr, StringExpr
        file.write(f"{spacing}{type(node).__name__}(value={node.value})\n")

    elif hasattr(node, 'name'):  # SymbolExpr u otros
        file.write(f"{spacing}{type(node).__name__}(name={node.name})\n")

    else:
        file.write(f"{spacing}{repr(node)}\n")