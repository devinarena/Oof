
########################################################################################
# File       : lexer.py
# Author     : Devin Arena
# Description: Lexes the file and returns a list of tokens.
# Since      : 5/1/2022
########################################################################################

def lex_file(file_path):
    with open(file_path, "r") as file:
        ops = []
        for row, line in enumerate(file):
            if line.startswith("#") or len(line) == 0 or line[0] == '\n':
                continue
            curr = []
            for col, token in lex_line(line):
                curr.append((file_path, row + 1, col, token))
            ops.append(curr)
    return ops


def lex_line(line: str) -> list:
    tokens = []
    col = 0
    while line[col].isspace():
        col += 1
    line = line[col:]
    while ' ' in line:
        space = line.index(' ')
        token = line[:space]
        tokens.append((col, token))
        col += space + 1
        line = line[space + 1:]
    token = ""
    if '\n' in line:
        token = line[:line.index('\n')]
    else:
        token = line
    tokens.append((col, token))
    return tokens
