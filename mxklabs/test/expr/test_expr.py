import unittest

import mxklabs as mxk


class Test_ExprComp(unittest.TestCase):

    def test_exprcomp_equal(self):

        # Test an exception is raised with different types.
        with self.assertRaises(Exception):
            mxk.Equals(mxk.Var('bool', 'v1'), mxk.Var('uint8', 'v2'))

        # Test NO exception gets raised with same types.
        mxk.Equals(mxk.Var('bool', 'v1'), mxk.Var('bool', 'v2'))
        mxk.Equals(mxk.Var('uint7', 'v1'), mxk.Var('uint7', 'v2'))
