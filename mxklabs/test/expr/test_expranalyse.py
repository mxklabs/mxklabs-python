import inspect
import unittest

import mxklabs as mxk

class Test_ExprWalker(unittest.TestCase):

  def test_expr_walker(self):

    class PrettyPrinter(mxk.ExprWalker):
      def to_string(self, expr): return self.bottom_up_walk(expr, None);

      def visit_variable(self, expr, res, args): return str(expr.id())

      def visit_constant(self, expr, res, args): return str(
        expr.value().user_value()).lower()

      def visit_logical_and(self, expr, res, args): return "(" + " AND ".join(
        [res[c] for c in expr.children()]) + ")"

      def visit_logical_or(self, expr, res, args): return "(" + " OR ".join(
        [res[c] for c in expr.children()]) + ")"

      def visit_logical_not(self, expr, res, args): return "(NOT" + res[
        expr.children()[0]] + ")"

    expr = mxk.LogicalAnd(
      mxk.Variable(type='bool', id="v1"),
      mxk.LogicalOr(
        mxk.Constant(type='bool', user_value=False),
        mxk.Variable(type='bool', id="v1")))

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
          mxk.utils.Utils.class_has_function(visitor_type, visit_method_name))


class Test_VariableHarvester(unittest.TestCase):
  
  def test_and(self):              
    getvars = mxk.VariableHarvester()
    
    # Check (logical-and (var v1) (const false)) simplifies to (const false)
    self.assertEqual(
      set([mxk.Variable(type='bool', id="v1")]),
      getvars.process(mxk.LogicalAnd(
        mxk.Variable(type='bool', id="v1"),
        mxk.Constant(type='bool', user_value=False))))

    # Check (logical-and (const true) (const true)) simplifies to (const false)
    self.assertEqual(
      set([mxk.Variable(type='bool', id="v1"),mxk.Variable(type='bool', id="v2")]),
      getvars.process(mxk.LogicalAnd(
        mxk.Variable(type='bool', id="v1"),
        mxk.Variable(type='bool', id="v2"),
        mxk.LogicalNot(mxk.Variable(type='bool', id="v1")))))


class Test_ConstantPropagator(unittest.TestCase):
  
  def test_and(self):              
    const_prop = mxk.ConstantPropagator()
    
    # Check (logical-and (var v1) (const false)) simplifies to (const false)
    self.assertEqual(
      mxk.Constant(type='bool', user_value=False),
      const_prop.process(mxk.LogicalAnd(
        mxk.Variable(type='bool', id="v1"),
        mxk.Constant(type='bool', user_value=False))))

    # Check (logical-and (const true) (const true)) simplifies to (const false)
    self.assertEqual(
      mxk.Constant(type='bool', user_value=True),
      const_prop.process(mxk.LogicalAnd(
        mxk.Constant(type='bool', user_value=True),
        mxk.Constant(type='bool', user_value=True))))

  def test_or(self):              
    const_prop = mxk.ConstantPropagator()
    
    # Check (logical-or (var v1) (const true) simplifies to (const true)
    self.assertEqual(
      mxk.Constant(type='bool', user_value=True),
      const_prop.process(mxk.LogicalOr(
        mxk.Variable(type='bool', id="v1"),
        mxk.Constant(type='bool', user_value=True))))

    # Check (logical-or (const false) (const false)) simplifies to (const false)
    self.assertEqual(
      mxk.Constant(type='bool', user_value=False),
      const_prop.process(mxk.LogicalOr(
        mxk.Constant(type='bool', user_value=False),
            mxk.Constant(type='bool', user_value=False))))

class Test_ExpressionEvaluator(unittest.TestCase):
  
  def test_expression_evaluator_and(self):

    v1_ = mxk.Variable(type='bool', id="v1")
    e_ = mxk.LogicalAnd(
      mxk.Variable(type='bool', id="v1"),
      mxk.Constant(type='bool', user_value=True))

    self.assertTrue(mxk.ExpressionEvaluator.process(e_, {v1_: mxk.ExprValue(type=mxk.ExprTypeRepository._BOOL, user_value=True)}).user_value())
    self.assertFalse(mxk.ExpressionEvaluator.process(e_, {v1_: mxk.ExprValue(type=mxk.ExprTypeRepository._BOOL, user_value=False)}).user_value())