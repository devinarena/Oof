

import sys
import os
import expr
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import token
import tokens

class ASTPrinter(expr.AST.Visitor):
    def print(self, expr: expr.AST) -> None:
        return expr.accept(self)

    def visit_binary(self, binary: expr.Binary) -> None:
        return self.parenthesize(binary.operator.lexeme, binary.left, binary.right)

    def visit_grouping(self, grouping: expr.Grouping) -> None:
        return self.parenthesize("group", grouping.expression)
    
    def visit_literal(self, literal: expr.Literal) -> None:
        if literal.value == "null":
            return "null"
        return str(literal.value)
    
    def visit_unary(self, unary: expr.Unary) -> None:
        return self.parenthesize(unary.operator.lexeme, unary.right)
    
    def parenthesize(self, name: str, *expr: expr.AST) -> None:
        s = f"({name}"

        for ex in expr:
            s += f" {ex.accept(self)}"
        
        s += ")"
        
        return s

if __name__ == "__main__":
    print(token)
    ex = expr.Binary(expr.Unary(token.Token(tokens.MINUS, "-", None, 1, 0), expr.Literal(123)), \
        token.Token(tokens.STAR, "*", None, 1, 1), \
        expr.Grouping(expr.Literal(45.68)))
    print(ASTPrinter().print(ex))