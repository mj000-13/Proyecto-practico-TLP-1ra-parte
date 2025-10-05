from Ast1.statements import ClassStatement, FunctionStatement, ReturnStatement


def print_ast(node, file, indent=0):
    spacing = '  ' * indent

    if isinstance(node, ClassStatement):
        file.write(f"{spacing}ClassStmt\n")
        file.write(f"{spacing}  name: {node.name}\n")
        file.write(f"{spacing}  attributes:\n")
        if node.attributes:
            for attr in node.attributes:
                print_ast(attr, file, indent + 2)
        else:
            file.write(f"{spacing}    (no attributes)\n")
        file.write(f"{spacing}  methods:\n")
        if node.methods:
            for method in node.methods:
                print_ast(method, file, indent + 2)
        else:
            file.write(f"{spacing}    (no methods)\n")

    elif isinstance(node, FunctionStatement):
        file.write(f"{spacing}FunctionStmt\n")
        file.write(f"{spacing}  name: {node.name}\n")
        file.write(f"{spacing}  params: {node.params}\n")
        file.write(f"{spacing}  body:\n")
        for stmt in node.body:
            print_ast(stmt, file, indent + 2)

    elif isinstance(node, ReturnStatement):
        file.write(f"{spacing}ReturnStmt\n")
        if node.value:
            file.write(f"{spacing}  value:\n")
            print_ast(node.value, file, indent + 2)
        else:
            file.write(f"{spacing}  value: None\n")

    elif hasattr(node, 'body'):  # BlockStmt
        file.write(f"{spacing}BlockStmt\n")
        file.write(f"{spacing}  body:\n")
        for stmt in node.body:
            print_ast(stmt, file, indent + 2)

    elif hasattr(node, 'expression'):  # ExpressionStmt
        file.write(f"{spacing}ExpressionStmt\n")
        file.write(f"{spacing}  expression:\n")
        print_ast(node.expression, file, indent + 2)

    elif hasattr(node, 'operator') and hasattr(node, 'left') and hasattr(node, 'right'):  # BinaryExpr
        file.write(f"{spacing}BinaryExpr(operator:{node.operator.lexeme})\n")
        file.write(f"{spacing}  left:\n")
        print_ast(node.left, file, indent + 2)
        file.write(f"{spacing}  right:\n")
        print_ast(node.right, file, indent + 2)


    elif hasattr(node, 'value') and not hasattr(node, 'assign'):  # NumberExpr, StringExpr
        file.write(f"{spacing}{type(node).__name__}(value:{node.value})\n")

    elif hasattr(node, 'name'):  # SymbolExpr u otros
        file.write(f"{spacing}{type(node).__name__}(name:{node.name})\n")

    elif hasattr(node, 'varname') and hasattr(node, 'isconstant') and hasattr(node, 'assignedvalue'):  # VarDeclStmt
        file.write(f"{spacing}VarDeclStmt\n")
        file.write(f"{spacing}  varname: {node.varname}\n")
        file.write(f"{spacing}  isconstant: {node.isconstant}\n")
        file.write(f"{spacing}  assignedvalue:\n")
        print_ast(node.assignedvalue, file, indent + 2)

    elif hasattr(node, "operator") and hasattr(node, "rightexpr"):
        file.write(f"{spacing}PrefixExpr(operator: {node.operator.lexeme})\n")
        file.write(f"{spacing}  rightexpr:\n")
        print_ast(node.rightexpr, file, indent + 2)



    elif hasattr(node, 'assign') and hasattr(node, 'operator') and hasattr(node, 'value'):  # AssignmentExpr
        file.write(f"{spacing}AssignmentExpr(operator:{node.operator.lexeme})\n")
        file.write(f"{spacing}  assign:\n")
        print_ast(node.assign, file, indent + 2)
        file.write(f"{spacing}  value:\n")
        print_ast(node.value, file, indent + 2)

    elif hasattr(node, 'elements'):  # ArrayExpr
        file.write(f"{spacing}ArrayExpr\n")
        file.write(f"{spacing}  elements:\n")
        for element in node.elements:
            print_ast(element, file, indent + 2)




    else:
        file.write(f"{spacing}{repr(node)}\n")
