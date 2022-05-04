
########################################################################################
# File       : tokens.py
# Author     : Devin Arena
# Description: Stores information regarding different token types in oof.
# Since      : 5/3/2022
########################################################################################

from http.client import FORBIDDEN


iota_c = 0

def iota(reset=False) -> int:
    global iota_c
    if reset:
        iota_c = 0
    res = iota_c
    iota_c += 1
    return res

# Single character tokens
LEFT_PAREN = iota()
RIGHT_PAREN = iota()
LEFT_BRACE = iota()
RIGHT_BRACE = iota()
COMMA = iota()
DOT = iota()
MINUS = iota()
PLUS = iota()
SEMI_COLON = iota()
SLASH = iota()
STAR = iota()

# Single or double character tokens
BANG = iota()
BANG_EQUAL = iota()
EQUAL = iota()
EQUAL_EQUAL = iota()
GREATER = iota()
GREATER_EQUAL = iota()
LESS = iota()
LESS_EQUAL = iota()

# LITERALS
IDENTIFIER = iota()
STRING = iota()
NUMBER = iota()

# Keywords
AND = iota()
CLASS = iota()
ELSE = iota()
FALSE = iota
FUN = iota()
FOR = iota()
IF = iota()
NULL = iota()
OR = iota()
OUTPUT = iota()
RETURN = iota()
SUPER = iota()
THIS = iota()
TRUE = iota()
SET = iota()
WHILE = iota()

EOF = iota()

keywords = {
    "and": AND,
    "class": CLASS,
    "else": ELSE,
    "false": FALSE,
    "fun": FUN,
    "for": FOR,
    "if": IF,
    "null": NULL,
    "or": OR,
    "output": OUTPUT,
    "return": RETURN,
    "super": SUPER,
    "this": THIS,
    "true": TRUE,
    "set": SET,
    "while": WHILE
}