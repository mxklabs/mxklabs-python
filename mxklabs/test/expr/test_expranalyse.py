import unittest

import mxklabs as mxk

class Test_VariableHarvester(unittest.TestCase):
  
  def test_and(self):              
    getvars = mxk.VariableHarvester()
    
    # Check (logical-and (var v1) (const false)) simplifies to (const false)
    self.assertEqual(
      set([mxk.Variable(mxk.Bool(), "v1")]),
      getvars.process(mxk.LogicalAnd(
        mxk.Variable(mxk.Bool(), "v1"),
        mxk.Constant(mxk.Bool(), user_value=False))))

    # Check (logical-and (const true) (const true)) simplifies to (const false)
    self.assertEqual(
      set([mxk.Variable(mxk.Bool(), "v1"),mxk.Variable(mxk.Bool(), "v2")]),
      getvars.process(mxk.LogicalAnd(
        mxk.Variable(mxk.Bool(), "v1"),
        mxk.Variable(mxk.Bool(), "v2"),
        mxk.LogicalNot(mxk.Variable(mxk.Bool(), "v1")))))

class Test_ConstantPropagator(unittest.TestCase):
  
  def test_and(self):              
    const_prop = mxk.ConstantPropagator()
    
    # Check (logical-and (var v1) (const false)) simplifies to (const false)
    self.assertEqual(
      mxk.Constant(mxk.Bool(), user_value=False), 
      const_prop.process(mxk.LogicalAnd(
        mxk.Variable(mxk.Bool(), "v1"),
        mxk.Constant(mxk.Bool(), user_value=False))))

    # Check (logical-and (const true) (const true)) simplifies to (const false)
    self.assertEqual(
      mxk.Constant(mxk.Bool(), user_value=True),                 
      const_prop.process(mxk.LogicalAnd(
        mxk.Constant(mxk.Bool(), user_value=True),
        mxk.Constant(mxk.Bool(), user_value=True))))

  def test_or(self):              
    const_prop = mxk.ConstantPropagator()
    
    # Check (logical-or (var v1) (const true) simplifies to (const true)
    self.assertEqual(
      mxk.Constant(mxk.Bool(), user_value=True), 
      const_prop.process(mxk.LogicalOr(
        mxk.Variable(mxk.Bool(), "v1"),
        mxk.Constant(mxk.Bool(), user_value=True))))

    # Check (logical-or (const false) (const false)) simplifies to (const false)
    self.assertEqual(
      mxk.Constant(mxk.Bool(), user_value=False),      
      const_prop.process(mxk.LogicalOr(
        mxk.Constant(mxk.Bool(), user_value=False),
            mxk.Constant(mxk.Bool(), user_value=False))))

class Test_ExpressionEvaluator(unittest.TestCase):
  
  def test_expression_evaluator_and(self):

    v1_ = mxk.Variable(mxk.Bool(), "v1")
    e_ = mxk.LogicalAnd(
      mxk.Variable(mxk.Bool(), "v1"),
      mxk.Constant(mxk.Bool(), user_value=True))

    self.assertTrue(mxk.ExpressionEvaluator.process(e_, {v1_: mxk.ExprValue(mxk.Bool(), user_value=True)}).user_value())
    self.assertFalse(mxk.ExpressionEvaluator.process(e_, {v1_: mxk.ExprValue(mxk.Bool(), user_value=False)}).user_value())