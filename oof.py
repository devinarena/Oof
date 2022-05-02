
########################################################################################
# File       : interpreter.py
# Author     : Devin Arena
# Description: Interpreter for the programming language, very primitive atm.
# Since      : 5/1/2022
########################################################################################

import sys

import lexer

# Registers
registers = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0
}

iota_c = 0

############################################
# Function   : iota
# Author     : Devin Arena
# Description: Simple iota counter logic.
# Since      : 5/1/2022
############################################


def iota(reset=False) -> int:
    global iota_c
    if reset:
        iota_c = 0
    res = iota_c
    iota_c += 1
    return res


OP_SET = iota()
OP_ADD = iota()
OP_SUB = iota()
OP_PRINT = iota()
OP_PRINT_CHAR = iota()


def set(register: str, value: int) -> None:
    return (OP_SET, register, value)


def add(regA: str, regB: str) -> None:
    return (OP_ADD, regA, regB)


def sub(regA: str, regB: str) -> None:
    return (OP_SUB, regA, regB)


def print_value(register: str) -> None:
    return (OP_PRINT, register)


def print_char(register: str) -> None:
    return (OP_PRINT_CHAR, register)


def interpret(program_calls: list) -> None:
    # Handle each operation in the program call
    for call in program_calls:
        if call[0] == OP_SET:
            registers[call[1]] = call[2]
        elif call[0] == OP_ADD:
            registers[call[1]] += registers[call[2]]
        elif call[0] == OP_SUB:
            registers[call[1]] -= registers[call[2]]
        elif call[0] == OP_PRINT:
            print(registers[call[1]], end='')
        elif call[0] == OP_PRINT_CHAR:
            print(chr(registers[call[1]]), end='')
        else:
            print("Unknown instruction")


def read_program(file: str) -> None:
    lines = lexer.lex_file(file)
    for line in lines:
        ops = [op[3] for op in line]
        if ops[0] == 'SET':
            program_calls.append(set(ops[1], int(ops[2])))
        elif ops[0] == 'PRINT':
            program_calls.append(print_value(ops[1]))
        elif ops[0] == 'ADD':
            program_calls.append(add(ops[1], ops[2]))
        elif ops[0] == 'SUB':
            program_calls.append(sub(ops[1], ops[2]))
        elif ops[0] == 'PRINTCHAR':
            program_calls.append(print_char(ops[1]))


program_calls = [
]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: oof.py <[c]ompile,[i]nterpret> <file>")
        exit(1)

    if sys.argv[1] == "c" or sys.argv[1] == "compile":
        print("ERROR: Compiler not written yet")
    elif sys.argv[1] == "i" or sys.argv[1] == "interpret":
        read_program(sys.argv[2])
        interpret(program_calls)
    else:
        print("Usage: oof.py <[c]ompile,[i]nterpret> <file>")
