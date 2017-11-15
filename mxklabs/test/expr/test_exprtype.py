import inspect
import unittest

import mxklabs as mxk

class Test_Bool(unittest.TestCase):

  def test_expr_type_bool(self):
    T = mxk.ExprTypeRepository._BOOL
    self.assertEqual("bool", str(T))
    self.assertEqual([False, True], [value.user_value() for value in T.values()])
    self.assertEqual([(False,), (True,)], [value.littup_value() for value in T.values()])
    self.assertEqual(2, T.num_values())

class Test_BitVector(unittest.TestCase):

  def test_expr_type_bool(self):
    T = mxk.ExprTypeRepository._BITVEC(8)
    self.assertEqual("uint8", str(T))
    self.assertEqual(list(range(2**8)), list([value.user_value() for value in
       T.values()]))
    # TODO(mkkt): Test littup values?
    self.assertEqual(2**8, T.num_values())
    self.assertEqual((False,False,False,False,False,True,True,True),
       T.user_value_to_littup_value(224))
    self.assertEqual(224, T.littup_value_to_user_value((False,False,False,False,
       False,True,True,True)))

    
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
    
  def test_expr_type_functions(self):
    
    # For all classes, exprtype_type, that derive from mxk.ExprType...
    for exprtype_type in mxk.Utils.get_derived_classes(mxk, mxk.ExprType):

      self.assertTrue(mxk.Utils.class_has_function(exprtype_type, 'user_value_to_littup_value'))
      self.assertTrue(mxk.Utils.class_has_function(exprtype_type, 'littup_value_to_user_value'))
      self.assertTrue(mxk.Utils.class_has_function(exprtype_type, 'is_valid_user_value'))
      self.assertTrue(mxk.Utils.class_has_function(exprtype_type, 'is_valid_littup_value'))

class Test_ExprTypeRepository(unittest.TestCase):

  def test_expr_type_repository(self):
    self.assertTrue(isinstance(mxk.ExprTypeRepository.get_expr_type_from_type_str('bool'), mxk.Bool))