import unittest

import mxklabs.expr as e

class Test_ConstProp(unittest.TestCase):
  
  def test_and(self):              
    const_prop = e.ConstProp()
    
    # Check (logical-and (var v1) (const false)) simplifies to (const false)
    self.assertEqual(
      e.Constant(e.Bool(), False), 
      const_prop.process(e.LogicalAnd(
        e.Variable(e.Bool(), "v1"),
        e.Constant(e.Bool(), False))))

    # Check (logical-and (const true) (const true)) simplifies to (const false)
    self.assertEqual(
      e.Constant(e.Bool(), True),                 
      const_prop.process(e.LogicalAnd(
        e.Constant(e.Bool(), True),
        e.Constant(e.Bool(), True))))

  def test_or(self):              
    const_prop = e.ConstProp()
    
    # Check (logical-or (var v1) (const true) simplifies to (const true)
    self.assertEqual(
      e.Constant(e.Bool(), True), 
      const_prop.process(e.LogicalOr(
        e.Variable(e.Bool(), "v1"),
        e.Constant(e.Bool(), True))))

    # Check (logical-or (const false) (const false)) simplifies to (const false)
    self.assertEqual(
      e.Constant(e.Bool(), False),      
      const_prop.process(e.LogicalOr(
        e.Constant(e.Bool(), False),
            e.Constant(e.Bool(), False))))