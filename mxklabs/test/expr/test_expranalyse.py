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
        mxk.Constant(mxk.Bool(), False))))

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
      mxk.Constant(mxk.Bool(), False), 
      const_prop.process(mxk.LogicalAnd(
        mxk.Variable(mxk.Bool(), "v1"),
        mxk.Constant(mxk.Bool(), False))))

    # Check (logical-and (const true) (const true)) simplifies to (const false)
    self.assertEqual(
      mxk.Constant(mxk.Bool(), True),                 
      const_prop.process(mxk.LogicalAnd(
        mxk.Constant(mxk.Bool(), True),
        mxk.Constant(mxk.Bool(), True))))

  def test_or(self):              
    const_prop = mxk.ConstantPropagator()
    
    # Check (logical-or (var v1) (const true) simplifies to (const true)
    self.assertEqual(
      mxk.Constant(mxk.Bool(), True), 
      const_prop.process(mxk.LogicalOr(
        mxk.Variable(mxk.Bool(), "v1"),
        mxk.Constant(mxk.Bool(), True))))

    # Check (logical-or (const false) (const false)) simplifies to (const false)
    self.assertEqual(
      mxk.Constant(mxk.Bool(), False),      
      const_prop.process(mxk.LogicalOr(
        mxk.Constant(mxk.Bool(), False),
            mxk.Constant(mxk.Bool(), False))))