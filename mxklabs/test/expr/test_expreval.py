import unittest

import mxklabs as mxk

class Test_ExprEvaluator(unittest.TestCase):

    def _TEST(self, exp_result, expr, variable_assignment_dict):
        """
        Internal helper function which tests that, given an Expr object, expr,
        and a variable assignment, variable_assignment, dict, that the
        ExprEvaluator returns exp_result.
        :param exp_result: A ExprValue object representing the expected
        evaluation result.
        :param expr: The Expr object to evaluate.
        :param variable_assignment_dict: The values of variables as a dict from
        Var objects to ExprValue object.
        """
        variable_assignment = lambda var : variable_assignment_dict[var]
        act_result = mxk.ExprEvaluator.eval(expr, variable_assignment)
        self.assertEqual(exp_result, act_result)

    def test_expreval_const(self):
        c1_ = mxk.Const('bool', True)
        c2_ = mxk.Const('bool', False)
        true_ = mxk.ExprValue('bool', True)
        false_ = mxk.ExprValue('bool', False)

        self._TEST(true_, c1_, {})
        self._TEST(false_, c2_, {})

    def test_expreval_var(self):
        v1_ = mxk.Var('bool', 'v1')
        v2_ = mxk.Var('uint8', 'v2')

        true_ = mxk.ExprValue('bool', True)
        false_ = mxk.ExprValue('bool', False)
        eight_ = mxk.ExprValue('uint8', 8)

        self._TEST(true_, v1_, {v1_: true_})
        self._TEST(false_, v1_, {v1_: false_})
        self._TEST(eight_, v2_, {v2_: eight_})

    def test_expreval_logical_and(self):
        v1_ = mxk.Var('bool', "v1")
        v2_ = mxk.Var('bool', "v2")
        true_ = mxk.ExprValue('bool', True)
        false_ = mxk.ExprValue('bool', False)

        e_ = mxk.LogicalAnd(v1_, v2_)

        self._TEST(true_, e_, {v1_: true_, v2_: true_})
        self._TEST(false_, e_, {v1_: true_, v2_: false_})
        self._TEST(false_, e_, {v1_: false_, v2_: true_})
        self._TEST(false_, e_, {v1_: false_, v2_: false_})

    def test_expreval_logical_or(self):

        v1_ = mxk.Var('bool', "v1")
        v2_ = mxk.Var('bool', "v2")
        true_ = mxk.ExprValue('bool', True)
        false_ = mxk.ExprValue('bool', False)

        e_ = mxk.LogicalOr(v1_, v2_)

        self._TEST(true_, e_, {v1_: true_, v2_: true_})
        self._TEST(true_, e_, {v1_: true_, v2_: false_})
        self._TEST(true_, e_, {v1_: false_, v2_: true_})
        self._TEST(false_, e_, {v1_: false_, v2_: false_})

    def test_expreval_logical_not(self):
        v1_ = mxk.Var('bool', "v1")
        true_ = mxk.ExprValue('bool', True)
        false_ = mxk.ExprValue('bool', False)

        e_ = mxk.LogicalNot(v1_)

        self._TEST(false_, e_, {v1_: true_})
        self._TEST(true_, e_, {v1_: false_})

    def test_expreval_equals(self):
        v1_ = mxk.Var('uint8', "v1")
        v2_ = mxk.Var('uint8', "v2")
        true_ = mxk.ExprValue('bool', True)
        false_ = mxk.ExprValue('bool', False)
        int76_ = mxk.ExprValue('uint8', 76)
        int122_ = mxk.ExprValue('uint8', 122)

        e_ = mxk.Equals(v1_, v2_)

        self._TEST(false_, e_, {v1_: int76_, v2_: int122_})
        self._TEST(true_, e_, {v1_: int76_, v2_: int76_})

