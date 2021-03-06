
########################################################################################
# File       : oof.py
# Author     : Devin Arena
# Description: Interpreter for the programming language, very primitive atm.
# Since      : 5/1/2022
########################################################################################

import sys
import os

import lexer
import parser
import interpreter
import resolver

import token
import tokens

import trees.astprinter

VERSION_MAJOR = 1
VERSION_MINOR = 0

ERROR = False
RUNTIME_ERROR = False

def runFile(file: str) -> None:
    if not os.path.exists(file):
        print("Error:: File not found")
        exit(1)
    with open(file, "r") as source:
        run(source.read())
    if ERROR:
        exit(65)
    if RUNTIME_ERROR:
        exit(70)

def run(source: str) -> None:
    lxr = lexer.Lexer(source)
    tokens = lxr.lex()
    psr = parser.Parser(tokens)
    stmnts = psr.parse()
    intr = interpreter.Interpreter()

    if ERROR:
        return

    rslv = resolver.Resolver(intr)
    rslv.resolve(stmnts)
    
    intr.interpret(stmnts)

def lex_error(msg: str, line: int, col: int) -> None:
    global ERROR
    ERROR = True
    print(f"Error:{line}:{col}:: {msg}")
    exit(1)

def error(token: token.Token, msg: str) -> None:
    global ERROR
    ERROR = True
    if token.type == tokens.EOF:
        print(f"Error:EOF:: {msg}")
    else:
        print(f"Error:{token.line}:{token.col}:: {msg}")
    exit(1)

def runtime_error(token: token.Token, msg: str) -> None:
    global RUNTIME_ERROR
    RUNTIME_ERROR = True
    print(f"Runtime Error:{token.line}:{token.col}:: {msg}")
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Oof v{VERSION_MAJOR}.{VERSION_MINOR} created by Devin Arena")
        print("Run oof --help for more information")
        exit(0)

    if sys.argv[1] == "--help":
        print(f"Oof v{VERSION_MAJOR}.{VERSION_MINOR} created by Devin Arena")
        print("Usage: oof.py <file>")
        exit(0)
    else:
        runFile(sys.argv[1])
