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




class Test_ConstProp(unittest.TestCase):

  def _TEST(self, exp_expr_out, expr_in):
    """
    Helper function that takes performs constant propagation on some input
    expression and tests equality to a given expected output.
    :param exp_expr_out: The expected output of constant propagation.
    :param expr_in: The input.
    """
    act_expr_out = mxk.ConstProp.process(expr_in)
    self.assertEqual(exp_expr_out, act_expr_out)

  def test_and(self):
    const_prop = mxk.ConstProp()

    # TODO(mkkt): Update.

    # Check (logical-and (var v1) (const false)) simplifies to (const false)
    self.assertEqual(
      mxk.Const(expr_type='bool', user_value=False),
      const_prop.process(mxk.LogicalAnd(
        mxk.Var(expr_type='bool', id="v1"),
        mxk.Const(expr_type='bool', user_value=False))))

    # Check (logical-and (const true) (const true)) simplifies to (const false)
    self.assertEqual(
      mxk.Const(expr_type='bool', user_value=True),
      const_prop.process(mxk.LogicalAnd(
        mxk.Const(expr_type='bool', user_value=True),
        mxk.Const(expr_type='bool', user_value=True))))

  def test_or(self):              
    const_prop = mxk.ConstProp()

    # TODO(mkkt): Update.
    
    # Check (logical-or (var v1) (const true) simplifies to (const true)
    self.assertEqual(
      mxk.Const(expr_type='bool', user_value=True),
      const_prop.process(mxk.LogicalOr(
        mxk.Var(expr_type='bool', id="v1"),
        mxk.Const(expr_type='bool', user_value=True))))

    # Check (logical-or (const false) (const false)) simplifies to (const false)
    self.assertEqual(
      mxk.Const(expr_type='bool', user_value=False),
      const_prop.process(mxk.LogicalOr(
        mxk.Const(expr_type='bool', user_value=False),
            mxk.Const(expr_type='bool', user_value=False))))

  # TODO(mkkt): Add tests for other expressions.
  # TODO(mkkt): Break out into seperate file?

  def test_constprop_equal(self):

    v1_ = mxk.Var('uint8', 'v1')
    v2_ = mxk.Var('uint8', 'v2')
    c1_ = mxk.Const('uint8', 84)
    c2_ = mxk.Const('uint8', 123)
    c3_ = mxk.Const('uint8', 84)

    self._TEST(mxk.Equals(v1_, v2_), mxk.Equals(v1_, v2_))
    self._TEST(mxk.Equals(v1_, c1_), mxk.Equals(v1_, c1_))
    self._TEST(mxk.Equals(c1_, v1_), mxk.Equals(c1_, v1_))
    self._TEST(mxk.Const('bool', False), mxk.Equals(c1_, c2_))
    self._TEST(mxk.Const('bool', True), mxk.Equals(c1_, c3_))
