import unittest

import mxklabs as mxk

#tseitin._print_cache()

#TRUE = mxk.TseitinCache.TRUE_LIT
#FALSE = mxk.TseitinCache.FALSE_LIT

class Test_Tseitin(unittest.TestCase):

    def _TEST(self, result, constraints):
        t = mxk.Tseitin()
        s = mxk.CryptoSatSolver(logger=lambda msg: None)
        for c in constraints:
            t.add_constraint(c)
        self.assertEqual(result, s.solve(t.dimacs()))

    def _TEST_SAT(self, constraints):
        self._TEST(mxk.SatSolver.RESULT_SAT, constraints)

    def _TEST_UNSAT(self, constraints):
        self._TEST(mxk.SatSolver.RESULT_UNSAT, constraints)

    def _to_set(self, list_of_lists):
        return set([frozenset(list) for list in list_of_lists])

    def _to_str(self, list_of_lists):
        return "\n".join(['[' + ','.join([str(lit) for lit in list]) + ']' for list in list_of_lists])
#
#  def _test_clauses(self, tseitin, expr, exp_clauses):
#    exp_clauses = self._to_set(exp_clauses)
#    cache_str = "\n".join(["{expr} -> {lit}".format(expr=expr, lit=lit) for expr, lit in tseitin._cache._cache.items()])
#    error_str = "Expected {expr} to result in clauses:\n\n{exp_clauses}\n\n but we got\n\n{act_clauses}\n\n with\n\n{cache_str}".format(
#      expr=expr,
#      exp_clauses=self._to_str(exp_clauses),
#      act_clauses=self._to_str(tseitin.dimacs().clauses),
#      cache_str=cache_str)
#    self.assertEqual(exp_clauses, tseitin.dimacs().clauses, error_str)
#
#  def test_tseitin_constant_true(self):
#    tseitin = mxk.Tseitin()
#    e_ = mxk.Const(expr_type='bool', user_value=True)
#    tseitin.add_constraint(e_)
#
#    exp_clauses = [[TRUE]]
#    self._test_clauses(tseitin, e_, exp_clauses)
#
#  def test_tseitin_constant_false(self):
#    tseitin = mxk.Tseitin()
#    e_ = mxk.Const(expr_type='bool', user_value=False)
#    tseitin.add_constraint(e_)
#
#    exp_clauses = [[TRUE],[FALSE]]
#    self._test_clauses(tseitin, e_, exp_clauses)
#
#  def test_tseitin_variable(self):
#    tseitin = mxk.Tseitin()
#    e_ = mxk.Var(expr_type='bool', id='x')
#    tseitin.add_constraint(e_)
#
#    exp_clauses = [[TRUE],[tseitin.cache_lookup(e_)[0]]]
#    self._test_clauses(tseitin, e_, exp_clauses)
#
#  def test_tseitin_logical_and(self):
#    tseitin = mxk.Tseitin()
#    x_ = mxk.Var(expr_type='bool', id='x')
#    y_ = mxk.Var(expr_type='bool', id='y')
#    e_ = mxk.LogicalAnd(x_, y_)
#    tseitin.add_constraint(e_)
#
#    exp_clauses = [
#      [TRUE],
#      [tseitin.cache_lookup(x_)[0]],
#      [tseitin.cache_lookup(y_)[0]]
#    ]
#    self._test_clauses(tseitin, e_, exp_clauses)

    def test_tseitin_const(self):
        true_ = mxk.Const('bool', True)
        false_ = mxk.Const('bool', False)
        v_ = mxk.Var('bool', 'v')

        self._TEST_SAT([mxk.Equals(v_, true_)])
        self._TEST_SAT([mxk.Equals(v_, false_)])

    def test_tseitin_const(self):
        true_ = mxk.Const('bool', True)
        false_ = mxk.Const('bool', False)

        self._TEST_UNSAT([false_])
        self._TEST_SAT([true_])

    def test_tseitin_logical_and(self):
        true_ = mxk.Const('bool', True)
        false_ = mxk.Const('bool', False)

        x_ = mxk.Var('bool', 'x')
        y_ = mxk.Var('bool', 'y')
        e_ = mxk.LogicalAnd(x_, y_)

        self._TEST_UNSAT([e_, mxk.Equals(x_, false_), mxk.Equals(y_, false_)])
        self._TEST_UNSAT([e_, mxk.Equals(x_, false_), mxk.Equals(y_, true_)])
        self._TEST_UNSAT([e_, mxk.Equals(x_, true_), mxk.Equals(y_, false_)])
        self._TEST_SAT([e_, mxk.Equals(x_, true_), mxk.Equals(y_, true_)])

    def test_tseitin_logical_or(self):
        true_ = mxk.Const('bool', True)
        false_ = mxk.Const('bool', False)

        x_ = mxk.Var('bool', 'x')
        y_ = mxk.Var('bool', 'y')
        e_ = mxk.LogicalOr(x_, y_)

        self._TEST_UNSAT([e_, mxk.Equals(x_, false_), mxk.Equals(y_, false_)])
        self._TEST_SAT([e_, mxk.Equals(x_, false_), mxk.Equals(y_, true_)])
        self._TEST_SAT([e_, mxk.Equals(x_, true_), mxk.Equals(y_, false_)])
        self._TEST_SAT([e_, mxk.Equals(x_, true_), mxk.Equals(y_, true_)])

    def test_tseitin_logical_not(self):
        true_ = mxk.Const('bool', True)
        false_ = mxk.Const('bool', False)

        x_ = mxk.Var('bool', 'x')
        e_ = mxk.LogicalNot(x_)

        self._TEST_SAT([e_, mxk.Equals(x_, false_)])
        self._TEST_UNSAT([e_, mxk.Equals(x_, true_)])

#  def test_tseitin_logical_not(self):
#    tseitin = mxk.Tseitin()
#    x_ = mxk.Var(expr_type='bool', id='x')
#    e_ = mxk.LogicalNot(x_)
#    tseitin.add_constraint(e_)
#
#    exp_clauses = [[TRUE],[-tseitin.cache_lookup(x_)[0]]]
#    self._test_clauses(tseitin, e_, exp_clauses)
#
#  def test_tseitin_equals(self):
#    c1_ = mxk.Const('uint3', 5)
#    c2_ = mxk.Const('uint3', 5)
#    c3_ = mxk.Const('uint3', 2)
#
#    self._TEST_SAT([mxk.Equals(c1_, c2_)])
#    self._TEST_UNSAT([mxk.LogicalNot(mxk.Equals(c1_, c2_))])
#    self._TEST_UNSAT([mxk.Equals(c2_, c3_)])
#    self._TEST_SAT([mxk.LogicalNot(mxk.Equals(c2_, c3_))])

