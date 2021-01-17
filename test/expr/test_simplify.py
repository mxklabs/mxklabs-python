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

  # logical_and(v1) => v1
  expr = ctx.expr.logical_and(v1)
  assert(ctx.util.simplify(expr) == v1)

  # logical_and(logical_not(v1), v1) => false
  expr = ctx.expr.logical_and(ctx.expr.logical_not(v1), v1)
  assert(ctx.util.simplify(expr) == false)

def test_logical_not():
  ctx = mxklabs.expr.ExprContext()

  v1 = ctx.variable(name='v1', valtype=ctx.valtype.bool())
  true = ctx.constant(value=1, valtype=ctx.valtype.bool())
  false = ctx.constant(value=0, valtype=ctx.valtype.bool())

  # Can't simplify variable op.
  expr = ctx.expr.logical_not(v1)
  assert(ctx.util.simplify(expr) == expr)

  # logical_not(true) => false
  expr = ctx.expr.logical_not(true)
  assert(ctx.util.simplify(expr) == false)

  # logical_not(false) => true
  expr = ctx.expr.logical_not(false)
  assert(ctx.util.simplify(expr) == true)

  # logical_not(logical_not(v1)) => v1
  expr = ctx.expr.logical_not(ctx.expr.logical_not(v1))
  assert(ctx.util.simplify(expr) == v1)

def test_logical_or():
  ctx = mxklabs.expr.ExprContext()

  v1 = ctx.variable(name='v1', valtype=ctx.valtype.bool())
  v2 = ctx.variable(name='v2', valtype=ctx.valtype.bool())
  true = ctx.constant(value=1, valtype=ctx.valtype.bool())
  false = ctx.constant(value=0, valtype=ctx.valtype.bool())

  # Can't simplify two variable ops.
  expr = ctx.expr.logical_or(v1, v2)
  assert(ctx.util.simplify(expr) == expr)

  # logical_or(v1, true) => true
  expr = ctx.expr.logical_or(v1, true)
  assert(ctx.util.simplify(expr) == true)

  # logical_or(false, false) => false
  expr = ctx.expr.logical_or(false, false)
  assert(ctx.util.simplify(expr) == false)

  # logical_or(false, v1) => v1
  expr = ctx.expr.logical_or(false, v1)
  assert(ctx.util.simplify(expr) == v1)

  # logical_or(v1) => v1
  expr = ctx.expr.logical_or(v1)
  assert(ctx.util.simplify(expr) == v1)

  # logical_and(logical_not(v1), v1) => true
  expr = ctx.expr.logical_or(ctx.expr.logical_not(v1), v1)
  assert(ctx.util.simplify(expr) == true)

def test_logical_xor():
  ctx = mxklabs.expr.ExprContext()

  v1 = ctx.variable(name='v1', valtype=ctx.valtype.bool())
  v2 = ctx.variable(name='v2', valtype=ctx.valtype.bool())
  true = ctx.constant(value=1, valtype=ctx.valtype.bool())
  false = ctx.constant(value=0, valtype=ctx.valtype.bool())

  # Can't simplify two variable ops.
  expr = ctx.expr.logical_xor(v1, v2)
  assert(ctx.util.simplify(expr) == expr)

  # logical_xor(true, false) => true
  expr = ctx.expr.logical_xor(true, false)
  assert(ctx.util.simplify(expr) == true)

  # logical_xor(true, true) => false
  expr = ctx.expr.logical_xor(true, true)
  assert(ctx.util.simplify(expr) == false)

  # logical_xor(v1, v1) => false
  expr = ctx.expr.logical_xor(v1, v1)
  assert(ctx.util.simplify(expr) == false)

  # logical_xor(v1, logical_not(v1)) => true
  expr = ctx.expr.logical_xor(v1, ctx.expr.logical_not(v1))
  assert(ctx.util.simplify(expr) == true)

  # logical_xor(v1, true) => logical_not(v1)
  expr = ctx.expr.logical_xor(v1, true)
  assert(ctx.util.simplify(expr) == ctx.expr.logical_not(v1))

  # logical_xor(logical_not(v1), true) => v1
  expr = ctx.expr.logical_xor(ctx.expr.logical_not(v1), true)
  assert(ctx.util.simplify(expr) == v1)

  # logical_xor(v1, false) => v1
  expr = ctx.expr.logical_xor(v1, false)
  assert(ctx.util.simplify(expr) == v1)

  # logical_xor(logical_not(v1), false) => logical_not(v1)
  expr = ctx.expr.logical_xor(ctx.expr.logical_not(v1), false)
  assert(ctx.util.simplify(expr) == ctx.expr.logical_not(v1))