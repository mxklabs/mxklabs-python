import unittest

import mxklabs as mxk

class Test_ExpressionEvaluator(unittest.TestCase):

    def test_expression_evaluator_and(self):
        v1_ = mxk.Var(expr_type='bool', id="v1")
        e_ = mxk.LogicalAnd(
            mxk.Var(expr_type='bool', id="v1"),
            mxk.Const(expr_type='bool', user_value=True))

        self.assertTrue(mxk.ExpressionEvaluator.process(e_, {
            v1_: mxk.ExprValue(expr_type=mxk.ExprTypeRepository._BOOL,
                               user_value=True)}).user_value())
        self.assertFalse(mxk.ExpressionEvaluator.process(e_, {
            v1_: mxk.ExprValue(expr_type=mxk.ExprTypeRepository._BOOL,
                               user_value=False)}).user_value())