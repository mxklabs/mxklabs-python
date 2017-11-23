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

    def test_expression_evaluator_and(self):
        v1_ = mxk.Var('bool', "v1")
        v2_ = mxk.Var('bool', "v2")
        true_ = mxk.ExprValue('bool', True)
        false_ = mxk.ExprValue('bool', False)

        e_ = mxk.LogicalAnd(v1_, v2_)

        self._TEST(true_, e_, {v1_: true_, v2_: true_})
        self._TEST(false_, e_, {v1_: true_, v2_: false_})
        self._TEST(false_, e_, {v1_: false_, v2_: true_})
        self._TEST(false_, e_, {v1_: false_, v2_: false_})