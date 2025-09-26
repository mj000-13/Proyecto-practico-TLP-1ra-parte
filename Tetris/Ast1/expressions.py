


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








