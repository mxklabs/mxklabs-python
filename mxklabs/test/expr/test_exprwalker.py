import unittest

import mxklabs as mxk

class Test_ExprWalker(unittest.TestCase):
  
  def test_expr_walker(self):
    
    class PrettyPrinter(mxk.Visitor):
      def to_string(self, expr): return self.bottom_up_walk(expr);
      
      def visit_variable(self, expr, args): return str(expr.id())
      def visit_constant(self, expr, args): return str(expr.value()[0]).lower()
      def visit_logical_and(self, expr, args): return "(" + " AND ".join([args[c] for c in expr.children()]) + ")"
      def visit_logical_or(self, expr, args): return "(" + " OR ".join([args[c] for c in expr.children()]) + ")"
      def visit_logical_not(self, expr, args): return "(NOT" + args[expr.children()[0]] + ")"
    
    expr = mxk.LogicalAnd(
      mxk.Variable(type=mxk.Bool(), id="v1"),
      mxk.LogicalOr(
        mxk.Constant(type=mxk.Bool(), value=(False,)), 
        mxk.Variable(type=mxk.Bool(), id="v1")))

    printer = PrettyPrinter()
    
    self.assertEqual(printer.to_string(expr), "(v1 AND (false OR v1))")
