
########################################################################################
# File       : oof.py
# Author     : Devin Arena
# Description: Interpreter for the programming language, very primitive atm.
# Since      : 5/1/2022
########################################################################################

import sys

import lexer

VERSION_MAJOR = 1
VERSION_MINOR = 0


def runFile(file: str) -> None:
    with open(file, "r") as source:
        run(source.read())

def run(source: str) -> None:
    lxr = lexer.Lexer(source)
    for token in lxr.lex():
        print(str(token))

def error(msg: str, line: int, col: int) -> None:
    print(f"Error:{line}:{col}:: {msg}")
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Oof v{VERSION_MAJOR}.{VERSION_MINOR} created by Devin Arena")
        print("Run oof --help for more information")
        exit(0)

    if sys.argv[1] == "--help":
        print(f"Oof v{VERSION_MAJOR}.{VERSION_MINOR} created by Devin Arena")
        print("Usage: oof.py <[i]nterpret> <file>")
        exit(0)
    elif sys.argv[1] == "c" or sys.argv[1] == "compile":
        print("ERROR: Compiler not written yet")
    elif sys.argv[1] == "i" or sys.argv[1] == "interpret":
        runFile(sys.argv[2])
    else:
        print(f"Oof v{VERSION_MAJOR}.{VERSION_MINOR} created by Devin Arena")
        print("Run oof --help for more information")
        exit(0)
