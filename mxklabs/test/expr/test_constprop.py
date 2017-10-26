import unittest

import mxklabs.expr as e

class Tests(unittest.TestCase):
  
  def test_and(self):              
    const_prop = e.ConstProp()
    
    # Check (and (var v1) (const false)) simplifies to (const false)
    self.assertEqual(
      e.Const(e.Bool, False), 
      const_prop.process(e.And([e.Var(e.Bool, "v1"),e.Const(e.Bool, False)])))

    # Check (and (var v1) (const false)) simplifies to (const false)
    self.assertEqual(
      e.Const(e.Bool, True), 
      const_prop.process(e.And([e.Const(e.Bool, True),e.Const(e.Bool, True)])))