import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import token

class Statement:
   class Visitor:
      def visit_block(self, block: object):
          pass
      def visit_expression(self, expression: object):
          pass
      def visit_output(self, output: object):
          pass
      def visit_set(self, set: object):
          pass
   def accept(self, visitor: object) -> object:
       pass

class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor: object) -> object:
        return visitor.visit_block(self)

class Expression(Statement):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor: object) -> object:
        return visitor.visit_expression(self)

class Output(Statement):
    def __init__(self, output):
        self.output = output

    def accept(self, visitor: object) -> object:
        return visitor.visit_output(self)

class Set(Statement):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: object) -> object:
        return visitor.visit_set(self)

