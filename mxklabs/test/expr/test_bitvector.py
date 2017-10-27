import unittest

import mxklabs.expr as e

class Test_Expr(unittest.TestCase):

  def test_BitVector(self):    
    T = e.BitVector(3)
    self.assertEqual("uint3", str(T))
    self.assertEqual([0,1,2,3,4,5,6,7], [value for value in T.values()])
    self.assertEqual(8, T.num_values())