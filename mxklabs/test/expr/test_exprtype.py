import inspect
import unittest

import mxklabs as mxk


class Test_Bool(unittest.TestCase):

    def test_exprtype_bool(self):
        T = mxk.ExprTypeRepository._BOOL
        self.assertEqual("bool", str(T))
        self.assertEqual([False, True], [value.user_value() for value in T.values()])
        self.assertEqual([(False,), (True,)], [value.littup_value() for value in T.values()])
        self.assertEqual(2, T.num_values())


class Test_BitVector(unittest.TestCase):

    def test_exprtype_bitvector(self):
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

        # Check 'bool' maps to _BOOL.
        self.assertEqual(mxk.ExprTypeRepository._BOOL,
            mxk.ExprTypeRepository.lookup('bool'))

        # Test we can instantiate a REALLY large bitvector. The worry is that
        # the implementation instantiates all values. There should be 2^2048
        # (a rediculously large number) values in a bitvector with a 2048 bit
        # bitvector. So let's make one (to test it isn't explicitly instantiating
        # all of those values, and iterate over a few.
        T = mxk.ExprTypeRepository._BITVEC(2048)

        values = T.values()
        self.assertEqual(0, next(values).user_value())
        self.assertEqual(1, next(values).user_value())

        # Check 'uintN' maps to _BITVEC(N).
        self.assertEqual(mxk.ExprTypeRepository._BITVEC(8),
            mxk.ExprTypeRepository.lookup('uint8'))
        self.assertEqual(mxk.ExprTypeRepository._BITVEC(64),
            mxk.ExprTypeRepository.lookup('uint64'))


class Test_Product(unittest.TestCase):
    def test_exprtype_bitvector(self):
        T1 = mxk.ExprTypeRepository._BITVEC(8)
        T2 = mxk.ExprTypeRepository._BOOL
        T = mxk.ExprTypeRepository._PRODUCT(T1, T2)




class Test_ExprType(unittest.TestCase):

    def test_exprtype_functions(self):

        # For all classes, exprtype_type, that derive from mxk.ExprType...
        for exprtype_type in mxk.Utils.get_derived_classes(mxk, mxk.ExprType):

            self.assertTrue(mxk.Utils.class_has_function(exprtype_type, 'user_value_to_littup_value'))
            self.assertTrue(mxk.Utils.class_has_function(exprtype_type, 'littup_value_to_user_value'))
            self.assertTrue(mxk.Utils.class_has_function(exprtype_type, 'is_valid_user_value'))
            self.assertTrue(mxk.Utils.class_has_function(exprtype_type, 'is_valid_littup_value'))


class Test_ExprTypeRepository(unittest.TestCase):

    def test_exprtype_repository(self):
        type_bool = mxk.ExprTypeRepository.lookup('bool')
        self.assertTrue(isinstance(type_bool, mxk.Bool))

        type_uint7 = mxk.ExprTypeRepository.lookup('uint7')
        self.assertTrue(isinstance(type_uint7, mxk.BitVec))
        self.assertEqual(7, type_uint7.littup_size())

        type_prod = mxk.ExprTypeRepository.lookup('(bool,uint54)')
        self.assertTrue(isinstance(type_prod, mxk.Product))
        self.assertEquals(2, len(type_prod.subtypes()))
        self.assertTrue(isinstance(type_prod.subtypes()[0], mxk.Bool))
        self.assertTrue(isinstance(type_prod.subtypes()[1], mxk.BitVec))
        self.assertEqual(54, type_prod.subtypes()[1].littup_size())
