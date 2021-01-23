import mxklabs.expr
import pytest

def test_solver_cnf():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_expr_def_set('mxklabs.expr.exprdefset.logical')

  a = ctx.variable(name="a", valtype=ctx.valtype.bool())

  ctx.add_constraint(ctx.expr.logical_or(a))
  result = ctx.solve()

  # Is satisfiable.
  assert(result)

  # Must have a=True
  varmap = result.get_varmap()
  assert(True == varmap[a])


def test_sat2():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_expr_def_set('mxklabs.expr.exprdefset.logical')#

  a = ctx.variable(name="a", valtype=ctx.valtype.bool())

  ctx.add_constraint(ctx.expr.logical_not(a))
  result = ctx.solve()

  # Is satisfiable.
  assert(result)

  # Must have a=False
  varmap = result.get_varmap()
  assert(False == varmap[a])


def test_sat3():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_expr_def_set('mxklabs.expr.exprdefset.logical')#

  a = ctx.variable(name="a", valtype=ctx.valtype.bool())

  ctx.add_constraint(ctx.expr.logical_and(a, ctx.expr.logical_not(a)))
  result = ctx.solve()

  # Is not satisfiable.
  assert(not result)


def test_sat4():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_expr_def_set('mxklabs.expr.exprdefset.logical')#

  a = ctx.variable(name="a", valtype=ctx.valtype.bool())
  b = ctx.variable(name="b", valtype=ctx.valtype.bool())
  tt = ctx.constant(value=1, valtype=ctx.valtype.bool())
  ff = ctx.constant(value=0, valtype=ctx.valtype.bool())

  ctx.add_constraint(ctx.expr.logical_xnor(a, tt))
  ctx.add_constraint(ctx.expr.logical_implies(a, b))
  ctx.add_constraint(ctx.expr.logical_xnor(b, ff))
  result = ctx.solve()

  # Is not satisfiable.
  assert(not result)

def test_sat5():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_expr_def_set('mxklabs.expr.exprdefset.bitvector')
  ctx.load_expr_def_set('mxklabs.expr.exprdefset.logical')

  a = ctx.variable(name="a", valtype=ctx.valtype.bitvector(width=8))
  b = ctx.variable(name="b", valtype=ctx.valtype.bool())

  ctx.add_constraint(ctx.expr.bitvector_to_bool(a, index=2))

  result = ctx.solve()

  # Is not satisfiable.
  assert(result)

  # Check bit 2 is set.
  varmap = result.get_varmap()
  assert((varmap[a] >> 2) & 1 == 1)








  # For all values, check

"""

def test_unsat1():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.bool.variable(name="a")

  ctx.add_constraint(ctx.bool.logical_and(a, ctx.bool.logical_not(a)))
  result = ctx.solve()

  # Is not satisfiable.
  assert(not result)

def test_sat3():
  ctx = mxklabs.expr.ExprContext()
  true = ctx.bool.constant(value=1)

  ctx.add_constraint(true)
  result = ctx.solve()

  # Is satisfiable.
  assert(result)

def test_unsat2():
  ctx = mxklabs.expr.ExprContext()
  true = ctx.bool.constant(value=0)

  ctx.add_constraint(true)
  result = ctx.solve()

  # Is satisfiable.
  assert(not result)
"""