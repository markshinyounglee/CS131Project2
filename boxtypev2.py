from enum import Enum
from intbase import InterpreterBase

# Creating a boxed type (or wrapper class)
# Enumerated type for our different language data types
class Type(Enum):
    INT = 1
    BOOL = 2
    STRING = 3
    NIL = 4


# Represents a value, which has a type and its value
class Value:
    def __init__(self, type, value=None):
        self.t = type
        self.v = value

    def value(self):
        return self.v

    def type(self):
        return self.t

    def set(self, other):
        self.t = other.t
        self.v = other.v

    def __str__(self):
        return get_printable(self)


def create_value(val):
    if isinstance(val, int) and not isinstance(val, bool):  # int is a supertype of bool
        # "The Boolean type is a subtype of the integer type, and Boolean values behave like the values 0 and 1"
        # https://docs.python.org/3.10/reference/datamodel.html#the-standard-type-hierarchy
        return Value(Type.INT, val)
    elif val is True:  # shouldn't be integer
        # we need this because in Python, 1 == True
        return Value(Type.BOOL, True)
    elif val is False:  # shouldn't be integer
        # we need this because in Python, any value not 1 is False 
        return Value(Type.BOOL, False)
    elif val is None:
        return Value(Type.NIL, None)
    elif isinstance(val, str):
        return Value(Type.STRING, val)
    else:
        raise ValueError("Unknown value type")


def get_printable(val):  # get custom printable values
    if val.type() == Type.INT:
        return str(val.value())
    if val.type() == Type.STRING:
        return val.value()
    if val.type() == Type.BOOL:
        if val.value() is True:
            return "true"
        return "false"
    if val.type() == Type.NIL:
        return "nil"
