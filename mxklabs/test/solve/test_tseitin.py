import unittest

import mxklabs as mxk

#tseitin._print_cache()

TRUE = mxk.TseitinCache.TRUE_LIT
FALSE = mxk.TseitinCache.FALSE_LIT

class Test_Tseitin(unittest.TestCase):
    
  def _to_set(self, list_of_lists):
    return set([frozenset(list) for list in list_of_lists])

  def _to_str(self, list_of_lists):
    return "\n".join(['[' + ','.join([str(lit) for lit in list]) + ']' for list in list_of_lists])  
  
  def _test_clauses(self, tseitin, expr, exp_clauses):
    exp_clauses = self._to_set(exp_clauses)
    cache_str = "\n".join(["{expr} -> {lit}".format(expr=expr, lit=lit) for expr, lit in tseitin._idcache.items()])
    error_str = "Expected {expr} to result in clauses:\n\n{exp_clauses}\n\n but we got\n\n{act_clauses}\n\n with\n\n{cache_str}".format(
      expr=expr,
      exp_clauses=self._to_str(exp_clauses),
      act_clauses=self._to_str(tseitin.dimacs().clauses),
      cache_str=cache_str)
    self.assertEqual(exp_clauses, tseitin.dimacs().clauses, error_str)
    
  def test_tseitin_constant_true(self):
    tseitin = mxk.Tseitin()
    e_ = mxk.Constant(type=mxk.Bool(), value=True)    
    tseitin.add_constraint(e_)
    
    exp_clauses = [[TRUE]]
    self._test_clauses(tseitin, e_, exp_clauses)

  def test_tseitin_constant_false(self):
    tseitin = mxk.Tseitin()
    e_ = mxk.Constant(type=mxk.Bool(), value=False)    
    tseitin.add_constraint(e_)
    
    exp_clauses = [[TRUE],[FALSE]]
    self._test_clauses(tseitin, e_, exp_clauses)

  def test_tseitin_variable(self):
    tseitin = mxk.Tseitin()
    e_ = mxk.Variable(type=mxk.Bool(), id='x')    
    tseitin.add_constraint(e_)
    
    exp_clauses = [[TRUE],[tseitin.cache_lookup(e_)]]
    self._test_clauses(tseitin, e_, exp_clauses)

  def test_tseitin_logical_and(self):
    tseitin = mxk.Tseitin()
    x_ = mxk.Variable(type=mxk.Bool(), id='x')
    y_ = mxk.Variable(type=mxk.Bool(), id='y')
    e_ = mxk.LogicalAnd(x_, y_)
    tseitin.add_constraint(e_)
    
    exp_clauses = [
      [TRUE],
      [tseitin.cache_lookup(x_)],
      [tseitin.cache_lookup(y_)]
    ]
    self._test_clauses(tseitin, e_, exp_clauses)
    
  def test_tseitin_logical_or(self):
    tseitin = mxk.Tseitin()
    x_ = mxk.Variable(type=mxk.Bool(), id='x')
    y_ = mxk.Variable(type=mxk.Bool(), id='y')
    e_ = mxk.LogicalOr(x_, y_)
    tseitin.add_constraint(e_)
    
    exp_clauses = [
      [TRUE],
      [tseitin.cache_lookup(e_)],
      [ tseitin.cache_lookup(e_),-tseitin.cache_lookup(x_)],
      [ tseitin.cache_lookup(e_),-tseitin.cache_lookup(y_)],
      [-tseitin.cache_lookup(e_), tseitin.cache_lookup(x_), tseitin.cache_lookup(y_)]
    ]
    self._test_clauses(tseitin, e_, exp_clauses)

  def test_tseitin_logical_not(self):
    tseitin = mxk.Tseitin()
    x_ = mxk.Variable(type=mxk.Bool(), id='x')
    e_ = mxk.LogicalNot(x_)
    tseitin.add_constraint(e_)
    
    exp_clauses = [[TRUE],[-tseitin.cache_lookup(x_)]]    
    self._test_clauses(tseitin, e_, exp_clauses)
