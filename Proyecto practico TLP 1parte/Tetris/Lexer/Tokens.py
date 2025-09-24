from enum import Enum, auto
from logging.config import IDENTIFIER
from token import NUMBER, STRING



"""CLASSES"""

# On the class kind we are goíng to find the types of tokens of our language


class TokenKind(Enum): # Enumerates the types of tokens, beginning with IOF = 0, NUMBER = 1, ...
    IOF = auto()
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    OPEN_BRAC = auto()  # [
    CLOSED_BRAC = auto()  # ]
    OPEN_CURL = auto()  # {
    CLOSED_CURL = auto()  # }
    OPEN_PARENT = auto()  # (
    CLOSED_PARENT = auto()  # )

    ASSINGMENT = auto()  # =
    EQUAL = auto()  # ==
    NOT = auto()  # !
    NOT_EQUAL = auto()  # !=

    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    OR = auto()
    AND = auto()

    DOT = auto()
    COLON = auto()
    COMMA = auto()
    SEMICOMMA = auto()
    QUESTION = auto()

    PLUS_PLUS = auto()  # ++
    MINUS_MINUS = auto()  # --
    PLUS_EQUAL = auto()  # +=
    MINUS_EQUAL = auto()  # -=

    PLUS = auto()
    DASH = auto()
    SLASH = auto()
    STAR = auto()
    PERCENT = auto()

    # Reserved words
    DEF = auto()
    CONST = auto()
    CLASS = auto()
    NEW = auto()
    IMPORT = auto()
    FROM = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    RANGE = auto()
    EXPORT = auto()
    TYPEOF = auto()
    RETURN = auto()

#A global dictionary for reserved words

reserved_lu ={
        "def": TokenKind.DEF,
        "return": TokenKind.RETURN,
        "const": TokenKind.CONST,
        "class":TokenKind.CLASS,
        "new":TokenKind.NEW,
        "import":TokenKind.IMPORT,
        "from":TokenKind.FROM,
        "if":TokenKind.IF,
        "else":TokenKind.ELSE,
        "while":TokenKind.WHILE,
        "for":TokenKind.FOR,
        "in":TokenKind.IN ,
        "range": TokenKind.RANGE,
        "export":TokenKind.EXPORT,
        "typeof":TokenKind.TYPEOF
    }




class Token:
    def __init__(self, tokenKind, value   ): #Define token as a type of token and a string value
        self.tokenKind = tokenKind
        self.value = value


"""----------------------------------------------------------------------------"""

"""GLOBAL FUNCTIONS"""
def newToken(kind , value ):
    return Token(kind,value)

def tokenKindString(kind): #Used in function debug to look for the TokenKind's attribute kind, and returns its string value
    return kind.name

def debug(tok): # If the type of the token is IDENTIFIER, NUMBER or STRING, it prints its string form, and its value.
    if tok.tokenKind in (TokenKind.IDENTIFIER, TokenKind.NUMBER, TokenKind.STRING):
        return "{} ({})".format(tokenKindString(tok.tokenKind), tok.value)
    else:
        return "{}".format(tokenKindString(tok.tokenKind))

"""----------------------------------------------------------------------------"""

"""EXAMPLE"""
#if __name__ == "__main__":
 #   t1 = newToken(TokenKind.NUMBER, "13413")
  #  print(debug(t1))