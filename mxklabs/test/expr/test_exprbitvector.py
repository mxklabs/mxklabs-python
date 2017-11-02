import unittest

import mxklabs as mxk

#class Test_Expr(unittest.TestCase):
#
#  def test_BitVector(self):    
#    T = e.BitVector(3)
#    self.assertEqual("uint3", str(T))
#    self.assertEqual([0,1,2,3,4,5,6,7], [value for value in T.values()])
#    self.assertEqual(8, T.num_values())
#    
#  def test_Index(self):
#    uint8 = e.BitVector(8)    
#    bitvector = e.Const(type=uint8, value=5)
#    index_0 = e.Const(type=uint8, value=0)
#    index_1 = e.Const(type=uint8, value=1)
#    index_2 = e.Const(type=uint8, value=2)
#    
#    values = \
#    {
#      bitvector: 5,
#      index_0: 0,
#      index_1: 1,
#      index_2: 2      
#    }
#    
#    expr_0 = e.Index(bitvector, index_0)
#    self.assertEqual(True, expr_0.evaluate(values))
#    expr_1 = e.Index(bitvector, index_1)
#    self.assertEqual(False, expr_1.evaluate(values))
    
    