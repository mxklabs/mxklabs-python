import unittest

import mxklabs as mxk

class Test_Expr(unittest.TestCase):

    def test_expr_str(self):
        self.assertEqual(
            str(mxk.LogicalAnd(
                mxk.Var(expr_type='bool', id="v1"),
                mxk.Var(expr_type='bool', id="v2"))),
            "(logical-and (var bool v1) (var bool v2))")

        self.assertEqual(
            str(mxk.LogicalAnd(
                mxk.Var(expr_type='bool', id="v1"),
                mxk.Const(expr_type='bool', user_value=True))),
            "(logical-and (var bool v1) (const bool true))")

        self.assertEqual(
            str(mxk.LogicalAnd(
                mxk.Var(expr_type='bool', id="v2"),
                mxk.Var(expr_type='bool', id="v1"))),
            "(logical-and (var bool v2) (var bool v1))")

        self.assertEqual(
            str(mxk.LogicalOr(
                mxk.Const(expr_type='bool', user_value=False),
                mxk.Var(expr_type='bool', id="v1"))),
            "(logical-or (const bool false) (var bool v1))")