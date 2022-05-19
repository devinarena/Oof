import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import token

class Statement:
   class Visitor:
      def visit_block(self, block: object):
          pass
      def visit_class_(self, class_: object):
          pass
      def visit_expression(self, expression: object):
          pass
      def visit_function(self, function: object):
          pass
      def visit_if_(self, if_: object):
          pass
      def visit_output(self, output: object):
          pass
      def visit_return_(self, return_: object):
          pass
      def visit_set(self, set: object):
          pass
      def visit_while_(self, while_: object):
          pass
   def accept(self, visitor: object) -> object:
       pass

class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor: object) -> object:
        return visitor.visit_block(self)

class Class_(Statement):
    def __init__(self, name, superclass, methods, fields):
        self.name = name
        self.superclass = superclass
        self.methods = methods
        self.fields = fields

    def accept(self, visitor: object) -> object:
        return visitor.visit_class_(self)

class Expression(Statement):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor: object) -> object:
        return visitor.visit_expression(self)

class Function(Statement):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: object) -> object:
        return visitor.visit_function(self)

class If_(Statement):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: object) -> object:
        return visitor.visit_if_(self)

class Output(Statement):
    def __init__(self, output):
        self.output = output

    def accept(self, visitor: object) -> object:
        return visitor.visit_output(self)

class Return_(Statement):
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: object) -> object:
        return visitor.visit_return_(self)

class Set(Statement):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: object) -> object:
        return visitor.visit_set(self)

class While_(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor: object) -> object:
        return visitor.visit_while_(self)

