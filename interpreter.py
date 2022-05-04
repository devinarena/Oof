
########################################################################################
# File       : interpreter.py
# Author     : Devin Arena
# Description: Interprets the expressions parse by the parser.
# Since      : 5/4/2022
########################################################################################

import sys
import os

import oof
import trees.expr
import trees.statement
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tokens
import token

class Interpreter(trees.expr.Expr.Visitor, trees.statement.Expr.Visitor):

    def interpret(self, statements: list) -> object:
        try:
            for statement in statements:
                self.execute(statement)
        except InterpreterError as e:
            oof.error(e.token, e.message)
    
    def visit_literal(self, literal: trees.expr.Literal) -> object:
        return literal.value
    
    def visit_grouping(self, grouping: trees.expr.Grouping) -> object:
        return self.evaluate(grouping.expression)
    
    def visit_unary(self, unary: object) -> object:
        right = self.evaluate(unary.right)
        if unary.operator.type == tokens.MINUS:
            self.check_number_op(right)
            return -right
        if unary.operator.type == tokens.BANG:
            return self.is_truthy(right)
        
        return None
    
    def visit_binary(self, binary: object) -> object:
        left = self.evaluate(binary.left)
        right = self.evaluate(binary.right)

        if binary.operator.type == tokens.MINUS:
            self.check_number_ops(binary.operator, left, right)
            return left - right
        if binary.operator.type == tokens.SLASH:
            self.check_number_ops(binary.operator, left, right)
            return left / right
        if binary.operator.type == tokens.STAR:
            self.check_number_ops(binary.operator, left, right)
            return left * right
        if binary.operator.type == tokens.PLUS:
            if type(left) is str and type(right) is str:
                return left + right
            elif type(left) is float and type(right) is float:
                return float(left) + float(right)
            elif type(left) is int and type(right) is int:
                return int(left) + int(right)
            else:
                return str(left) + str(right)
            # raise InterpreterError(binary.operator, "Operands must be two numbers or two strings")
        if binary.operator.type == tokens.GREATER:
            self.check_number_ops(binary.operator, left, right)
            return left > right
        if binary.operator.type == tokens.GREATER_EQUAL:
            self.check_number_ops(binary.operator, left, right)
            return left >= right
        if binary.operator.type == tokens.LESS:
            self.check_number_ops(binary.operator, left, right)
            return left < right
        if binary.operator.type == tokens.LESS_EQUAL:
            self.check_number_ops(binary.operator, left, right)
            return left <= right
        if binary.operator.type == tokens.BANG_EQUAL:
            return not self.is_equal(left, right)
        if binary.operator.type == tokens.EQUAL_EQUAL:
            return self.is_equal(left, right)

        return None
    
    def visit_expression(self, expression: trees.expr.Expr) -> object:
        return self.evaluate(expression.expression)

    def visit_output(self, expression: trees.expr.Expr) -> object:
        val = self.evaluate(expression.output)
        print(self.stringify(val))
        return None
    
    def is_truthy(self, value: object) -> bool:
        if value == None:
            return False
        if type(value) is bool:
            return value
        if type(value) is float:
            return value > 0.000001
        if type(value) is str:
            return len(str) > 0
        return True
    
    def is_equal(self, left: object, right: object):
        if left == None and right == None:
            return True
        if left == None:
            return False

        return left == right
    
    def check_number_op(self, operator: token.Token, operand: object) -> None:
        if type(operand) is not float:
            raise InterpreterError(operator, "Operand must be a number")
        
    def check_number_ops(self, operator: token.Token, left: object, right: object) -> None:
        if type(left) is not float or type(right) is not float:
            raise InterpreterError(operator, "Operands must be a number")
        
    def execute(self, statement: trees.statement.Expr) -> None:
        statement.accept(self)
        
    def evaluate(self, expr: trees.expr.Expr) -> object:
        return expr.accept(self)
    
    def stringify(self, obj: object) -> str:
        if obj == None:
            return "null"
        
        if type(obj) is float:
            s = str(obj)
            if s.endswith(".0"):
                s = s.split(".")[0]
            return s
        
        if type(obj) is bool:
            return str(obj).lower()
        
        return str(obj)

class InterpreterError(Exception):
    
    def __init__(self, token: token.Token, message: str):
        super().__init__(message)
        self.message = message
        self.token = token
        