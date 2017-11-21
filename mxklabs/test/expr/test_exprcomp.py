import unittest

import mxklabs as mxk

class Test_ExprComp(unittest.TestCase):

    def test_exprcomp_equal(self):

        with self.assertRaises(Exception):
            mxk.Equals(mxk.Var('bool', 'v1'), mxk.Var('uint8', 'v2'))