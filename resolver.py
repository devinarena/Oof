
########################################################################################
# File       : resolver.py
# Author     : Devin Arena
# Description: Handles the resolution of variables and functions
# Since      : 5/7/2022
########################################################################################

from socket import SocketIO

from idna import check_label
import trees.expr
import trees.statement
import token
import tokens
import errors

import oof

class Resolver(trees.expr.Expr.Visitor, trees.statement.Statement.Visitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_fuction = tokens.FTYPE_NONE
        self.current_class = tokens.CTYPE_NONE
    
    def visit_block(self, block: trees.statement.Block) -> object:
        self.begin_scope()
        self.resolve(block.statements)
        self.end_scope()
    
    
    def visit_class_(self, class_: trees.statement.Class_) -> object:
        enclosing_class = self.current_class
        self.current_class = tokens.CTYPE_CLASS

        self.declare(class_.name)
        self.define(class_.name)

        if class_.superclass:
            self.current_class = tokens.CTYPE_SUBCLASS
            if class_.superclass.name.lexeme == class_.name.lexeme:
                oof.error(class_.name, "Classes can't inherit from themselves")
            self.resolve_(class_.superclass)

            self.begin_scope()
            self.scopes[-1]["super"] = True

        self.begin_scope()
        self.scopes[-1]["this"] = True

        for method in class_.methods:
            declaration = tokens.FTYPE_METHOD
            if method.name.lexeme == "init":
                declaration = tokens.FTYPE_CONSTRUCTOR
            self.resolve_function(method, declaration)
        
        self.end_scope()

        if class_.superclass:
            self.end_scope()

        self.current_class = enclosing_class

        return None
    
    def visit_set(self, set: trees.statement.Set) -> object:
        self.declare(set.name)
        if set.initializer:
            self.resolve_(set.initializer)
        self.define(set.name)
        return None
    
    def visit_super(self, super: trees.expr.Super) -> object:
        if self.current_class == tokens.CTYPE_NONE:
            oof.error(super.keyword, "Cannot use 'super' outside of a class")
        elif self.current_class != tokens.CTYPE_SUBCLASS:
            oof.error(super.keyword, "Cannot use 'super' in a class with no superclass")
        
        self.resolve_local(super, super.keyword)
        return None
    
    def visit_variable(self, variable: trees.expr.Variable) -> object:
        if self.scopes and not self.scopes[-1].get(variable.name.lexeme, True):
            oof.error(variable.name, "Cannot read local variable in its own initializer")
        
        self.resolve_local(variable, variable.name)
        return None
    
    def visit_this(self, this: trees.expr.This) -> object:
        if self.current_class == tokens.CTYPE_NONE:
            oof.error(this.keyword, "Cannot use 'this' outside of a class")
            return None
        self.resolve_local(this, this.keyword)
        return None
    
    def visit_assign(self, assign: trees.expr.Assign) -> object:
        self.resolve__(assign.value)
        self.resolve_local(assign, assign.name)
        return None
    
    def visit_function(self, function: trees.statement.Function) -> object:
        self.declare(function.name)
        self.define(function.name)

        self.resolve_function(function, tokens.FTYPE_FUNCTION)
        return None
    
    def visit_get(self, get: trees.expr.Get) -> object:
        self.resolve_(get.object)
        return None
    
    def visit_set_(self, set: trees.expr.Set_) -> object:
        self.resolve_(set.value)
        self.resolve_(set.object)
        return None
    
    def declare(self, name: token.Token) -> None:
        if not self.scopes:
            return

        scope = self.scopes[-1]
        if name.lexeme in scope:
            oof.error(name, "Variable with this name already declared in this scope")
        scope[name.lexeme] = False
    
    def define(self, name: token.Token) -> None:
        if not self.scopes:
            return

        scope = self.scopes[-1]
        scope[name.lexeme] = True
        
    def resolve_function(self, function: trees.statement.Function, type: int) -> None:
        enclosing_function = self.current_fuction
        self.current_fuction = type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve(function.body)
        self.end_scope()
        self.current_fuction = enclosing_function
    
    def resolve_local(self, expr: token.Token, name: token.Token) -> None:
        for i in range(len(self.scopes) - 1, -1, -1):
            scope = self.scopes[i]
            if name.lexeme in scope:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
    
    def resolve(self, statements) -> None:
        for statement in statements:
            self.resolve_(statement)
    
    def resolve_(self, statement) -> None:
        statement.accept(self)
    
    def resolve__(self, expr) -> None:
        expr.accept(self)
    
    def begin_scope(self) -> None:
        self.scopes.append({})
    
    def end_scope(self) -> None:
        self.scopes.pop()

    def visit_expression(self, expression: trees.statement.Expression) -> object:
        self.resolve_(expression.expression)
    
    def visit_if_(self, if_: trees.statement.If_) -> object:
        self.resolve(if_.condition)
        self.resolve_(if_.then_branch)
        if if_.else_branch:
            self.resolve_(if_.else_branch)
        return None
    
    def visit_output(self, output: trees.statement.Output) -> object:
        self.resolve_(output.output)
        return None
    
    def visit_return_(self, return_: trees.statement.Return_) -> object:
        if self.current_fuction == tokens.FTYPE_NONE:
            oof.error(return_.keyword, "Cannot return from top-level code")

        if return_.value:
            if self.current_fuction == tokens.FTYPE_CONSTRUCTOR:
                oof.error(return_.keyword, "Constructors always return 'this'")

            self.resolve_(return_.value)
        
        return None
    
    def visit_while_(self, while_: trees.statement.While_) -> object:
        self.resolve_(while_.condition)
        self.resolve(while_.body)
        return None
    
    def visit_binary(self, binary: trees.expr.Binary) -> object:
        self.resolve_(binary.left)
        self.resolve_(binary.right)
        return None
    
    def visit_call(self, call: trees.expr.Call) -> object:
        self.resolve_(call.callee)

        for arg in call.args:
            self.resolve_(arg)
        
        return None
    
    def visit_grouping(self, grouping: trees.expr.Grouping) -> object:
        self.resolve_(grouping.expression)
        return None
    
    def visit_literal(self, literal: trees.expr.Literal) -> object:
        return None
    
    def visit_logical(self, logical: trees.expr.Logical) -> object:
        self.resolve_(logical.left)
        self.resolve_(logical.right)
        return None
    
    def visit_unary(self, unary: trees.expr.Unary) -> object:
        self.resolve_(unary.right)
        return None