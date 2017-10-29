import unittest

import mxklabs.expr as e

class Test_Type(unittest.TestCase):

  def test_Bool(self):   
    T = e.Bool()
    self.assertEqual("bool", str(T))
    self.assertEqual([False, True], [value for value in T.values()])
    self.assertEqual(2, T.num_values())
    
  def test_Product(self):    
    T = e.Product([e.BitVector(2),e.Bool()])
    self.assertEqual("(uint2,bool)", str(T))
    self.assertEqual(set([
      (e.BitVector.int_to_value(2, 0), False), 
      (e.BitVector.int_to_value(2, 0), True), 
      (e.BitVector.int_to_value(2, 1), False), 
      (e.BitVector.int_to_value(2, 1), True), 
      (e.BitVector.int_to_value(2, 2), False), 
      (e.BitVector.int_to_value(2, 2), True), 
      (e.BitVector.int_to_value(2, 3), False), 
      (e.BitVector.int_to_value(2, 3), True)]), set([value for value in T.values()]))
    self.assertEqual(8, T.num_values())
