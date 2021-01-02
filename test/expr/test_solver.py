import mxklabs.expr
import pytest

def test_sat1():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.prop.variable(name="a")

  ctx.add_constraint(a)
  result = ctx.solve()

  # Is satisfiable.
  assert(result)
  # Must have a=True
  varmap = result.get_varmap()
  assert(True == varmap[a])

def test_sat2():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.prop.variable(name="a")

  ctx.add_constraint(ctx.prop.logical_not(a))
  result = ctx.solve()

  # Is satisfiable.
  assert(result)
  # Must have a=False
  varmap = result.get_varmap()
  assert(False == varmap[a])

def test_unsat1():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.prop.variable(name="a")

  ctx.add_constraint(ctx.prop.logical_and(a, ctx.prop.logical_not(a)))
  result = ctx.solve()

  # Is not satisfiable.
  assert(not result)

