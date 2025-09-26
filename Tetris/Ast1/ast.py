from abc import ABC, abstractmethod

class Stmt(ABC):
    @abstractmethod
    def stmt(self):
        pass

class Expr(ABC):
    @abstractmethod
    def expr(self):
        pass



