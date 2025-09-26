from enum import IntEnum, auto

class BindingPower(IntEnum):
    default_bp = 0
    comma = auto()
    assignment = auto()
    logical = auto()
    relational = auto()
    additive = auto()
    multiplicative = auto()
    unary = auto()
    call = auto()
    member = auto()
    primary = auto()