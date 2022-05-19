
########################################################################################
# File       : interpreter.py
# Author     : Devin Arena
# Description: Interprets the expressions parse by the parser.
# Since      : 5/4/2022
########################################################################################

import sys
import os
import time

import oof
import environment
import oofinstance
import trees.expr
import trees.statement
import errors
import callable
import ooffunction
import oofclass
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tokens
import token

class Interpreter(trees.expr.Expr.Visitor, trees.statement.Statement.Visitor):

    def __init__(self) -> None:
        super().__init__()
        self.locals = {}
        self.globals = environment.Environment()
        self.env = self.globals

        class Clock(callable.Callable):
            def call(self, interpreter: Interpreter, args: list) -> object:
                return time.time()
            def __str__(self) -> str:
                return "<clock fn>"
        self.globals.define("clock", Clock())

    def interpret(self, statements: list) -> object:
        try:
            for statement in statements:
                self.execute(statement)
        except errors.InterpreterError as e:
            oof.error(e.token, e.message)
    
    def visit_literal(self, literal: trees.expr.Literal) -> object:
        return literal.value
    
    def visit_grouping(self, grouping: trees.expr.Grouping) -> object:
        return self.evaluate(grouping.expression)
    
    def visit_set_(self, set: trees.expr.Set_) -> object:
        obj = self.evaluate(set.object)
        if type(obj) is not oofinstance.OofInstance:
            raise errors.InterpreterError(set.name, f"Object '{obj}' does not have property '{set.name.lexeme}'")
        value = self.evaluate(set.value)
        obj.set(set.name, value)
        return value
    
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
    
    def visit_call(self, call: trees.expr.Call) -> object:
        callee = self.evaluate(call.callee)

        args = []
        for arg in call.args:
            args.append(self.evaluate(arg))

        if not issubclass(callee.__class__, callable.Callable):
            raise errors.InterpreterError(call.paren, "Can only call functions and classes")
        if len(args) != callee.arity():
            raise errors.InterpreterError(call.paren, f"Expected {callee.arity()} arguments but got {len(args)}")
        return callee.call(self, args)
    
    def visit_get(self, get: trees.expr.Get) -> object:
        obj = self.evaluate(get.object)
        if type(obj) is not oofinstance.OofInstance:
            raise errors.InterpreterError(get.name, f"Object '{obj}' does not have property '{get.name.lexeme}'")
        return obj.get(get.name)

    def visit_logical(self, logical: object) -> object:
        left = self.evaluate(logical.left)

        if logical.operator.type == tokens.OR:
            if self.is_truthy(left):
                return left
        if logical.operator.type == tokens.AND:
            if not self.is_truthy(left):
                return left
        
        return self.evaluate(logical.right)

    def visit_block(self, block: trees.statement.Block) -> object:
        self.execute_block(block.statements, environment.Environment(self.env))

    def visit_class_(self, class_: trees.statement.Class_) -> object:
        superclass = None
        if class_.superclass:
            superclass = self.evaluate(class_.superclass)
            if type(superclass) is not oofclass.OofClass:
                raise errors.InterpreterError(class_.name, f"Superclass must be a class")

        self.env.define(class_.name.lexeme, None)

        if class_.superclass:
            self.env = environment.Environment(self.env)
            self.env.define("super", superclass)

        methods = {}
        for method in class_.methods:
            fun = ooffunction.OofFunction(method, self.env, method.name.lexeme == "init")
            methods[method.name.lexeme] = fun
        
        if class_.superclass:
            self.env = self.env.enclosing

        self.env.assign(class_.name, oofclass.OofClass(class_.name.lexeme, superclass, methods))
        return None
    
    def visit_this(self, this: trees.expr.This) -> object:
        return self.lookup_variable(this.keyword, this)
    
    def visit_expression(self, expression: trees.statement.Expression) -> object:
        return self.evaluate(expression.expression)

    def visit_output(self, output: trees.expr.Expr) -> object:
        val = self.evaluate(output.output)
        print(self.stringify(val))
        return None
    
    def visit_super(self, super_: trees.expr.Super) -> object:
        distance = self.locals.get(super_, None)
        if distance is None:
            raise errors.InterpreterError(super_.keyword, "Cannot use 'super' outside of a class")
        superclass = self.env.get_at(distance, "super")
        object = self.env.get_at(distance - 1, "this")
        method = superclass.find_method(super_.method.lexeme)
        if method is None:
            raise errors.InterpreterError(super_.method, f"Undefined property '{super_.method.lexeme}'")
        return method.bind(object)
    
    def visit_set(self, set: trees.statement.Set) -> object:
        value = None
        if set.initializer != None:
            value = self.evaluate(set.initializer)
        self.env.define(set.name.lexeme, value)
        return None
    
    def visit_function(self, func: trees.statement.Function) -> object:
        func_ = ooffunction.OofFunction(func, self.env, False)
        self.env.define(func.name.lexeme, func_)
        return None
    
    def visit_variable(self, variable: trees.expr.Variable) -> object:
        return self.lookup_variable(variable.name, variable)
    
    def visit_assign(self, assign: trees.expr.Assign) -> object:
        value = self.evaluate(assign.value)

        distance = self.locals.get(assign.name)
        if distance:
            self.env.assign_at(distance, assign.name, value)
        else:
            self.globals.assign(assign.name, value)
        
        return value
    
    def visit_if_(self, iff: trees.statement.If_) -> object:
        if self.is_truthy(self.evaluate(iff.condition)):
            self.execute(iff.then_branch)
        elif iff.else_branch:
            self.execute(iff.else_branch)
        return None
    
    def visit_return_(self, return_: object) -> object:
        value = None

        if return_.value != None:
            value = self.evaluate(return_.value)
        raise errors.Return(value)
    
    def visit_while_(self, while_: trees.statement.While_) -> None:
        while self.is_truthy(self.evaluate(while_.condition)):
            self.execute(while_.body)
        
        return None
    
    def execute_block(self, statements: list, env: environment.Environment) -> None:
        previous = self.env

        try:
            self.env = env

            for statement in statements:
                self.execute(statement)
        finally:
            self.env = previous
    
    def lookup_variable(self, name: token.Token, expr: trees.expr.Expr) -> object:
        distance = self.locals.get(expr)

        if distance == None:
            return self.globals.get(name)
        else:
            return self.env.get_at(distance, name.lexeme)
    
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
            raise errors.InterpreterError(operator, "Operand must be a number")
        
    def check_number_ops(self, operator: token.Token, left: object, right: object) -> None:
        if type(left) is not float or type(right) is not float:
            raise errors.InterpreterError(operator, "Operands must be a number")
        
    def execute(self, statement: trees.statement.Statement) -> None:
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
        
    def resolve(self, expr: trees.expr.Expr, depth: int) -> object:
        self.locals[expr] = depth