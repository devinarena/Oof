
########################################################################################
# File       : lexer.py
# Author     : Devin Arena
# Description: Lexes the file and returns a list of tokens.
# Since      : 5/1/2022
########################################################################################

import tokens
import token
import oof

class Lexer:
    def __init__(self, source) -> None:
        self.source = source
        self.token_list = []

        self.start = 0
        self.current = 0
        self.line = 1
        self.col = 0

    def lex(self) -> list:
        # Reset, though this should not be called more than once
        self.token_list.clear()
        
        self.start = 0
        self.current = 0
        self.line = 1
        self.col = 0

        while not self.at_end():
            self.start = self.current
            self.lex_token()
        
        self.token_list.append(token.Token(tokens.EOF, "", None, self.line, 0))
        return self.token_list

    def lex_token(self) -> None:
        c = self.next()
        # Handle special case for comments
        if c == "/":
            if self.match("/"):
                while not self.at_end() and self.peek() != "\n":
                    self.next()
            else:
                self.add_token(tokens.SLASH, None)
        # whitespace
        elif c == " " or c == "\r" or c == "\t":
            pass
        elif c == "\n":
            self.line += 1
            self.col = 0
        # One character tokens
        elif c == "(":
            self.add_token(tokens.LEFT_PAREN, None)
        elif c == ")":
            self.add_token(tokens.RIGHT_PAREN, None)
        elif c == "{":
            self.add_token(tokens.LEFT_BRACE, None)
        elif c == "}":
            self.add_token(tokens.RIGHT_BRACE, None)
        elif c == ",":
            self.add_token(tokens.COMMA, None)
        elif c == ".":
            self.add_token(tokens.DOT, None)
        elif c == "-":
            self.add_token(tokens.MINUS, None)
        elif c == "+":
            self.add_token(tokens.PLUS, None)
        elif c == ";":
            self.add_token(tokens.SEMI_COLON, None)
        elif c == "*":
            self.add_token(tokens.STAR, None)
        # One or more character tokens
        elif c == "!":
            self.add_token(tokens.BANG_EQUAL if self.match("=") else tokens.BANG, None)
        elif c == "=":
            self.add_token(tokens.EQUAL_EQUAL if self.match("=") else tokens.EQUAL, None)
        elif c == "<":
            if self.match("="):
                self.add_token(tokens.LESS_EQUAL, None)
            elif self.match("<"):
                self.add_token(tokens.EXTENDS, None)
            else:
                self.add_token(tokens.LESS, None)
        elif c == ">":
            self.add_token(tokens.GREATER_EQUAL if self.match("=") else tokens.GREATER, None)
        # Literals
        elif c == '"':
            self.lex_string()
        elif str.isdigit(c):
            self.lex_number()
        elif self.valid_identifier(c):
            self.lex_identifier()
        else:
            oof.lex_error("Unknown character", self.line, self.col)
    
    def lex_string(self) -> None:
        while not self.at_end() and self.peek() != '"':
            if self.peek() == "\n":
                self.line += 1
                self.col = 0
            self.next()
        
        if self.at_end():
            oof.lex_error("String is never terminated", self.line, self.col)
        
        self.next()
        literal = self.source[self.start + 1:self.current - 1]
        self.add_token(tokens.STRING, literal)

    def lex_number(self) -> None:
        while self.peek().isdigit():
            self.next()
        
        if self.peek() == "." and self.peek_next().isdigit():
            self.next()
            while self.peek().isdigit():
                self.next()
        
        literal = float(self.source[self.start:self.current])
        self.add_token(tokens.NUMBER, literal)
    
    def lex_identifier(self) -> None:
        while self.valid_identifier(self.peek()):
            self.next()
        
        lexeme = self.source[self.start:self.current]
        if lexeme in tokens.keywords:
            self.add_token(tokens.keywords[lexeme], None)
        else:
            self.add_token(tokens.IDENTIFIER, None)

    def at_end(self):
        return self.current >= len(self.source)

    def add_token(self, type: str, literal: object):
        lexeme = self.source[self.start:self.current]
        self.token_list.append(token.Token(type, lexeme, literal, self.line, self.col))

        self.col += len(lexeme)

    def next(self) -> str:
        c = self.source[self.current]

        self.current += 1
        return c
    
    def match(self, exp: str) -> bool:
        if self.at_end():
            return False
        if self.source[self.current] != exp:
            return False

        self.current += 1
        return True
    
    def peek(self) -> str:
        if self.at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
    
    def valid_identifier(self, target: str) -> str:
        return target.isalpha() or target.isdigit() or target == "_"