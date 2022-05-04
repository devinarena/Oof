

########################################################################################
# File       : token.py
# Author     : Devin Arena
# Description: Stores information about a particular token.
# Since      : 5/3/2022
########################################################################################

class Token:
    def __init__(self, type: int, lexeme: str, literal: object, line: int, col: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.col = col

    def __str__(self):
        return f'Token({self.type}, {self.lexeme}, {self.literal}, {self.line}, {self.col})'