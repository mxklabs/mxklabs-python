import unittest

import mxklabs as mxk

class Test_VarExtract(unittest.TestCase):
    def test_and(self):

        # Check (logical-and (var v1) (const false)) simplifies to (const false)
        self.assertEqual(
            set([mxk.Var(expr_type='bool', id="v1")]),
            mxk.VarExtractor.extract(mxk.LogicalAnd(
                mxk.Var(expr_type='bool', id="v1"),
                mxk.Const(expr_type='bool', user_value=False))))

        # Check (logical-and (const true) (const true)) simplifies to (const false)
        self.assertEqual(
            set([mxk.Var(expr_type='bool', id="v1"),
                 mxk.Var(expr_type='bool', id="v2")]),
            mxk.VarExtractor.extract(mxk.LogicalAnd(
                mxk.Var(expr_type='bool', id="v1"),
                mxk.Var(expr_type='bool', id="v2"),
                mxk.LogicalNot(mxk.Var(expr_type='bool', id="v1")))))