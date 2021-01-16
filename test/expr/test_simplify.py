import mxklabs.expr
import pytest

def test_logical_and():
  ctx = mxklabs.expr.ExprContext()

  v1 = ctx.variable(name='v1', valtype=ctx.valtype.bool())
  v2 = ctx.variable(name='v2', valtype=ctx.valtype.bool())
  true = ctx.constant(value=1, valtype=ctx.valtype.bool())
  false = ctx.constant(value=0, valtype=ctx.valtype.bool())

  # Can't simplify two variable ops.
  expr = ctx.expr.logical_and(v1, v2)
  assert(ctx.util.simplify(expr) == expr)

  # logical_and(v1, false) => false
  expr = ctx.expr.logical_and(v1, false)
  assert(ctx.util.simplify(expr) == false)

  # logical_and(true, true) => true
  expr = ctx.expr.logical_and(true, true)
  assert(ctx.util.simplify(expr) == true)

  # logical_and(true, v1) => v1
  expr = ctx.expr.logical_and(true, v1)
  assert(ctx.util.simplify(expr) == v1)

  # logical_and(logical_not(v1), v1) => false
  expr = ctx.expr.logical_and(ctx.expr.logical_not(v1), v1)
  assert(ctx.util.simplify(expr) == false)

