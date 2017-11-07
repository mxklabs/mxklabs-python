import unittest

import mxklabs as mxk

class Test_Type(unittest.TestCase):

  def test_Bool(self):   
    T = mxk.Bool()
    self.assertEqual("bool", str(T))
    self.assertEqual([(False,), (True,)], [value for value in T.values()])
    self.assertEqual(2, T.num_values())
    
  def test_Product(self):    
    T = mxk.Product([mxk.BitVector(2),mxk.Bool()])
    self.assertEqual("(uint2,bool)", str(T))
    self.assertEqual(set([
      (mxk.BitVector.int_to_value(2, 0), (False,)), 
      (mxk.BitVector.int_to_value(2, 0), (True,)), 
      (mxk.BitVector.int_to_value(2, 1), (False,)), 
      (mxk.BitVector.int_to_value(2, 1), (True,)), 
      (mxk.BitVector.int_to_value(2, 2), (False,)), 
      (mxk.BitVector.int_to_value(2, 2), (True,)), 
      (mxk.BitVector.int_to_value(2, 3), (False,)), 
      (mxk.BitVector.int_to_value(2, 3), (True,))]), set([value for value in T.values()]))
    self.assertEqual(8, T.num_values())
