import inspect
import unittest

import mxklabs as mxk

class Test_ExprType(unittest.TestCase):

  def test_exprtype_bool(self):   
    T = mxk.Bool()
    self.assertEqual("bool", str(T))
    self.assertEqual([(False,), (True,)], [value for value in T.values()])
    self.assertEqual(2, T.num_values())
    
  #def test_exprtype_product(self):    
  #  T = mxk.Product([mxk.BitVector(2),mxk.Bool()])
  #  self.assertEqual("(uint2,bool)", str(T))
  #  self.assertEqual(set([
  #    (mxk.BitVector.int_to_value(2, 0), (False,)), 
  #    (mxk.BitVector.int_to_value(2, 0), (True,)), 
  #    (mxk.BitVector.int_to_value(2, 1), (False,)), 
  #    (mxk.BitVector.int_to_value(2, 1), (True,)), 
  #    (mxk.BitVector.int_to_value(2, 2), (False,)), 
  #    (mxk.BitVector.int_to_value(2, 2), (True,)), 
  #    (mxk.BitVector.int_to_value(2, 3), (False,)), 
  #    (mxk.BitVector.int_to_value(2, 3), (True,))]), set([value for value in T.values()]))
  #  self.assertEqual(8, T.num_values())
    
  def test_exprtype_value_conversion(self):
    
    # For all classes, exprtype_type, that derive from mxk.ExprType...
    for exprtype_type in mxk.Utils.get_derived_classes(mxk, mxk.ExprType):

      # Test that exprtype_type has a function user_friendly_value_to_littup_value.
      error_msg = "'{classname}' does not have a member function called {method_name} " \
                  "(it is expected to because of parent class 'ExprType')".format(
        classname=exprtype_type.__name__,
        method_name='user_friendly_value_to_littup_value')
      
      self.assertTrue(hasattr(exprtype_type, 'user_friendly_value_to_littup_value'), error_msg)
      self.assertTrue(inspect.isfunction(getattr(exprtype_type, 'user_friendly_value_to_littup_value')), error_msg)

      # Test that exprtype_type has a function littup_value_to_user_friendly_value.
      error_msg = "'{classname}' does not have a member function called {method_name} " \
                  "(it is expected to because of parent class 'ExprType')".format(
        classname=exprtype_type.__name__,
        method_name='littup_value_to_user_friendly_value')
      
      self.assertTrue(hasattr(exprtype_type, 'littup_value_to_user_friendly_value'), error_msg)
      self.assertTrue(inspect.isfunction(getattr(exprtype_type, 'littup_value_to_user_friendly_value')), error_msg)
