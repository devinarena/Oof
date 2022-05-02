
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
            line = line.lstrip()
            if line.startswith("#") or len(line) == 0 or line[0] == '\n':
                continue
            curr = []
            for col, token in lex_line(line):
                curr.append((file_path, row, col, token))
            ops.append(curr)
    return ops


def lex_line(line: str) -> list:
    tokens = []
    for token in line.split():
        tokens.append((line.find(token), token))
    return tokens
