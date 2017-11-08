import inspect
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

  def test_expr_walker_functions(self):
    
    # For all classes, visitor_type, that derive from mxk.Visitor...    
    for visitor_type in mxk.Utils.get_derived_classes(mxk, mxk.Visitor):
      # For all classes, expr_type, that derive from mxk.Expr...
      for expr_type in mxk.Utils.get_derived_classes(mxk, mxk.Expr):
        # Test that visitor_type handles expr_type.
        visit_method_name = 'visit_' + mxk.Utils.camel_case_to_snake_case(expr_type.__name__)
        error_msg = "'{classname}' does not have a member function called {method_name} " \
                    "(it is expected to because of parent class 'Visitor')".format(
          classname=visitor_type.__name__,
          method_name=visit_method_name)
        
        self.assertTrue(hasattr(visitor_type, visit_method_name), error_msg)
        self.assertTrue(inspect.isfunction(getattr(visitor_type, visit_method_name)), error_msg)
        
        #result = visit_method(self, args)
    
        #has_attr = 
    