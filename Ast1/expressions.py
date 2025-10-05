


#--------------------------------------------------
class NumberExpr:
    def __init__(self, value):
        self.value = value
    def expr(self):
        pass

class StringExpr:
    def __init__(self, value):
        self.value = value
    def expr(self):
        pass

class SymbolExpr:
    def __init__(self, value):
        self.value = value
    def expr(self):
        pass
#--------------------------------------------------

class BinaryExpr:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def expr(self):
        pass

class PrefixExpr:
    def __init__(self, operator, rightexpr):
        self.operator = operator
        self.rightexpr = rightexpr

    def expr(self):
        pass

class AssignmentExpr:
    def __init__(self, assign, operator, value):
        self.assign = assign
        self.operator = operator
        self.value = value

    def expr(self):
        pass

class ArrayExpr:
    def __init__(self, elements):
        self.elements = elements

    def expr(self):
        pass






