
class BlockStmt:
    def __init__(self, body): # Body es un array
        self.body = body
    def stmt(self):
        pass


class ExpressionStmt:
    def __init__(self, expression):
        self.expression = expression
    def stmt(self):
        pass

class VarDeclStmt:
    def __init__(self, varname, isconstant, assignedvalue):
        self.varname = varname
        self.isconstant = isconstant
        self.assignedvalue = assignedvalue
    def stmt(self):
        pass

class ClassStatement:
    def __init__(self, name,attributes=None, methods=None):
        self.name = name
        self.attributes = attributes if attributes is not None else []
        self.methods = methods if methods is not None else []
    def stmt(self):
        pass

class FunctionStatement:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def stmt(self):
        pass

class ReturnStatement:
    def __init__(self, value):
        self.value = value  # puede ser una expresión o None
    def stmt(self):
        pass