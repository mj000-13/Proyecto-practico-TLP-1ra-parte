from abc import ABC, abstractmethod

# The Ast is 

class Stmt(ABC):
    @abstractmethod
    def stmt(self):
        pass

class Expr(ABC):
    @abstractmethod
    def expr(self):
        pass



