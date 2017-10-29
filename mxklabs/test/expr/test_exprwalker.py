import unittest

import mxklabs.expr as e

class Test_ExprWalker(unittest.TestCase):
  
  def test_expr_walker(self):
    
    class PrettyPrinter(e.Visitor):
      def to_string(self, expr): return self.bottom_up_walk(expr);
      
      def visit_variable(self, expr, args): return str(expr.id)
      def visit_constant(self, expr, args): return str(expr.value()).lower()
      def visit_logical_and(self, expr, args): return "(" + " AND ".join([args[c] for c in expr.children()]) + ")"
      def visit_logical_or(self, expr, args): return "(" + " OR ".join([args[c] for c in expr.children()]) + ")"
      def visit_logical_not(self, expr, args): return "(NOT" + args[expr.children()[0]] + ")"
    
    expr = e.LogicalAnd(
      e.Variable(type=e.Bool(), id="v1"),
      e.LogicalOr(
        e.Constant(type=e.Bool(), value=False), 
        e.Variable(type=e.Bool(), id="v1")))

    printer = PrettyPrinter()
    
    self.assertEqual(printer.to_string(expr), "(v1 AND (false OR v1))")
