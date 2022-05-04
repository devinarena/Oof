import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import token

class AST:
   class Visitor:
      def visit_binary(self, binary: object):
          pass
      def visit_grouping(self, grouping: object):
          pass
      def visit_literal(self, literal: object):
          pass
      def visit_unary(self, unary: object):
          pass
   def accept(self, visitor: object) -> None:
       pass

class Binary(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: object) -> None:
        visitor.visit_binary(self)

class Grouping(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: object) -> None:
        visitor.visit_grouping(self)

class Literal(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: object) -> None:
        visitor.visit_literal(self)

class Unary(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: object) -> None:
        visitor.visit_unary(self)

