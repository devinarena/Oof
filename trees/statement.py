import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import token

class Expr:
   class Visitor:
      def visit_expression(self, expression: object):
          pass
      def visit_output(self, output: object):
          pass
   def accept(self, visitor: object) -> object:
       pass

class Expression(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor: object) -> object:
        return visitor.visit_expression(self)

class Output(Expr):
    def __init__(self, output):
        self.output = output

    def accept(self, visitor: object) -> object:
        return visitor.visit_output(self)

