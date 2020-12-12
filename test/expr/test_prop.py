import mxklabs.expr
import pytest

def test_evaluate_not():
  ctx = mxklabs.expr.ExprContext()

  a = ctx.prop.variable(name="a")
  expr = ctx.prop.logical_not(a)

  assert(True == expr.evaluate({a : False}))
  assert(False == expr.evaluate({a : True}))

def test_evaluate_and():
  ctx = mxklabs.expr.ExprContext()

  a = ctx.prop.variable(name="a")
  b = ctx.prop.variable(name="b")
  expr = ctx.prop.logical_and(a, b)

  assert(False == expr.evaluate({a : False, b : False}))
  assert(False == expr.evaluate({a : False, b : True}))
  assert(False == expr.evaluate({a : True, b : False}))
  assert(True == expr.evaluate({a : True, b : True}))

def test_evaluate_or():
  ctx = mxklabs.expr.ExprContext()

  a = ctx.prop.variable(name="a")
  b = ctx.prop.variable(name="b")
  expr = ctx.prop.logical_or(a, b)

  assert(False == expr.evaluate({a : False, b : False}))
  assert(True == expr.evaluate({a : False, b : True}))
  assert(True == expr.evaluate({a : True, b : False}))
  assert(True == expr.evaluate({a : True, b : True}))

def test_expr_hash():
  ctx = mxklabs.expr.ExprContext()

  a1 = ctx.prop.variable(name="a")
  b1 = ctx.prop.variable(name="b")
  not1 = ctx.prop.logical_not(a1)
  not2 = ctx.prop.logical_not(a1)
  and1 = ctx.prop.logical_and(a1, b1)
  and2 = ctx.prop.logical_and(a1, b1)
  or1 = ctx.prop.logical_or(a1, b1)
  or2 = ctx.prop.logical_or(a1, b1)

  assert(hash(not1) == hash(not2))
  assert(hash(and1) == hash(and2))
  assert(hash(or1) == hash(or2))

  assert(hash(a1) != hash(b1))
  assert(hash(a1) != hash(not1))
  assert(hash(a1) != hash(and1))
  assert(hash(a1) != hash(or1))
  assert(hash(b1) != hash(not1))
  assert(hash(b1) != hash(and1))
  assert(hash(b1) != hash(or1))
  assert(hash(not1) != hash(and1))
  assert(hash(not1) != hash(or1))
  assert(hash(and1) != hash(or1))

def test_expr_pool():
  ctx = mxklabs.expr.ExprContext()
  a1 = ctx.prop.variable(name="a")
  not1 = ctx.prop.logical_not(a1)
  not2 = ctx.prop.logical_not(a1)
  assert(id(a1) != id(not2))
  assert(id(not1) == id(not2))

def test_expr_transform():
  ctx1 = mxklabs.expr.ExprContext(load_mxklabs_exprsets=False)
  ctx1.load_exprset("mxklabs.expr.exprsets.prop")

  a = ctx1.prop.variable(name="a")
  b = ctx1.prop.variable(name="b")
  expr = ctx1.prop.logical_or(a, b)

  ctx2 = mxklabs.expr.ExprContext(load_mxklabs_exprsets=False)
  ctx2.load_exprset("mxklabs.expr.exprsets.cnf")

  #ctx_mapping = ctx1.map_onto(ctx2)


ctx = mxklabs.expr.ExprContext()
a1 = ctx.prop.variable(name="a")
not1 = ctx.prop.logical_not(a1)
not2 = ctx.prop.logical_not(a1)
assert(id(a1) != id(not2))
assert(id(not1) == id(not2))

