import unittest

import mxklabs as mxk

# TODO: We're not checking that subexpressions are 'replaced' even when the
# top-level expression can't be reduced to a constant.

class Test_ConstPropagator(unittest.TestCase):
    def _TEST(self, exp_expr_out, expr_in):
        """
        Helper function that takes performs constant propagation on some input
        expression and tests equality to a given expected output.
        :param exp_expr_out: The expected output of constant propagation.
        :param expr_in: The input.
        """
        act_expr_out = mxk.ConstPropagator.propagate(expr_in)
        self.assertEqual(exp_expr_out, act_expr_out)

    def test_constprop_and(self):
        v1_ = mxk.Var('bool', 'v1')
        v2_ = mxk.Var('bool', 'v2')
        true_ = mxk.Const('bool', True)
        false_ = mxk.Const('bool', False)

        self._TEST(mxk.LogicalAnd(v1_, v2_), mxk.LogicalAnd(v1_, v2_))
        self._TEST(mxk.LogicalAnd(v1_, true_), mxk.LogicalAnd(v1_, true_))
        self._TEST(false_, mxk.LogicalAnd(v1_, false_))
        self._TEST(true_, mxk.LogicalOr(true_, true_))

    def test_constprop_or(self):
        v1_ = mxk.Var('bool', 'v1')
        v2_ = mxk.Var('bool', 'v2')
        true_ = mxk.Const('bool', True)
        false_ = mxk.Const('bool', False)

        self._TEST(mxk.LogicalOr(v1_, v2_), mxk.LogicalOr(v1_, v2_))
        self._TEST(mxk.LogicalOr(v1_, false_), mxk.LogicalOr(v1_, false_))
        self._TEST(false_, mxk.LogicalOr(false_, false_))
        self._TEST(true_, mxk.LogicalOr(v1_, true_))

    def test_constprop_not(self):
        v1_ = mxk.Var('bool', 'v1')
        true_ = mxk.Const('bool', True)
        false_ = mxk.Const('bool', False)

        self._TEST(mxk.LogicalNot(v1_), mxk.LogicalNot(v1_))
        self._TEST(false_, mxk.LogicalNot(true_))
        self._TEST(true_, mxk.LogicalNot(false_))

    def test_constprop_equal(self):
        v1_ = mxk.Var('uint8', 'v1')
        v2_ = mxk.Var('uint8', 'v2')
        c1_ = mxk.Const('uint8', 84)
        c2_ = mxk.Const('uint8', 123)
        c3_ = mxk.Const('uint8', 84)

        self._TEST(mxk.Equals(v1_, v2_), mxk.Equals(v1_, v2_))
        self._TEST(mxk.Equals(v1_, c1_), mxk.Equals(v1_, c1_))
        self._TEST(mxk.Equals(c1_, v1_), mxk.Equals(c1_, v1_))
        self._TEST(mxk.Const('bool', False), mxk.Equals(c1_, c2_))
        self._TEST(mxk.Const('bool', True), mxk.Equals(c1_, c3_))
