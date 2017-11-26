import inspect
import unittest

import mxklabs as mxk

class Test_ExprAnalyse(unittest.TestCase):

  def test_expr_walker(self):

    class PrettyPrinter(mxk.ExprWalker):
      def to_string(self, expr): return self.bottom_up_walk(expr, None);

      def visit_var(self, expr, res, args): return str(expr.id())

      def visit_const(self, expr, res, args): return str(
        expr.expr_value().user_value()).lower()

      def visit_logical_and(self, expr, res, args): return "(" + " AND ".join(
        [res[c] for c in expr.children()]) + ")"

      def visit_logical_or(self, expr, res, args): return "(" + " OR ".join(
        [res[c] for c in expr.children()]) + ")"

      def visit_logical_not(self, expr, res, args): return "(NOT" + res[
        expr.children()[0]] + ")"

    expr = mxk.LogicalAnd(
      mxk.Var(expr_type='bool', id="v1"),
      mxk.LogicalOr(
        mxk.Const(expr_type='bool', user_value=False),
        mxk.Var(expr_type='bool', id="v1")))

    printer = PrettyPrinter()

    self.assertEqual(printer.to_string(expr), "(v1 AND (false OR v1))")

  def test_expr_walker_functions(self):

    # For all classes, visitor_type, that derive from mxk.ExprWalker...
    for visitor_type in mxk.Utils.get_derived_classes(mxk, mxk.ExprWalker):
      # For all classes, expr_type, that derive from mxk.Expr...
      for expr_type in mxk.Utils.get_derived_classes(mxk, mxk.Expr):
        # Test that visitor_type handles expr_type.
        visit_method_name = 'visit_' + mxk.Utils.camel_case_to_snake_case(
          expr_type.__name__)

        self.assertTrue(
          mxk.utils.Utils.class_has_function(visitor_type, visit_method_name),
            "expected '{}' to have a function '{}'".format(
              visitor_type.__name__, visit_method_name))

  def test_expranalysis_expr_visitor_functions(self):

    # For all classes, visitor_type, that derive from mxk.ExprWalker...
    for visitor_type in mxk.Utils.get_derived_classes(mxk,
                                                      mxk.ExprVisitor):
      # For all classes, expr_type, that derive from mxk.Expr...
      for expr_type in mxk.Utils.get_derived_classes(mxk, mxk.Expr):
        # Test that visitor_type handles expr_type.
        visit_method_name = '_visit_' + mxk.Utils.camel_case_to_snake_case(
          expr_type.__name__)

        self.assertTrue(
          mxk.utils.Utils.class_has_function(visitor_type,
                                             visit_method_name),
          "expected '{}' to have a function '{}'".format(
            visitor_type.__name__, visit_method_name))



