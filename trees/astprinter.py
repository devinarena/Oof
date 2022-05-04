

import sys
import os
import trees.expr
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import token
import tokens

class ASTPrinter(trees.expr.Expr.Visitor):

    def print(self, expr: trees.expr.Expr) -> trees.expr.Expr:
        return expr.accept(self)

    def visit_binary(self, binary: trees.expr.Binary) -> str:
        return self.parenthesize(binary.operator.lexeme, binary.left, binary.right)

    def visit_grouping(self, grouping: trees.expr.Grouping) -> str:
        return self.parenthesize("group", grouping.expression)
    
    def visit_literal(self, literal: trees.expr.Literal) -> str:
        if literal.value == "null":
            return "null"
        return str(literal.value)
    
    def visit_unary(self, unary: trees.expr.Unary) -> str:
        return self.parenthesize(unary.operator.lexeme, unary.right)
    
    def parenthesize(self, name: str, *expr: trees.expr.Expr) -> str:
        s = f"({name}"

        for ex in expr:
            s += f" {ex.accept(self)}"
        
        s += ")"
        
        return s