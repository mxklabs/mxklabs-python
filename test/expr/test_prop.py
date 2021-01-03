import mxklabs.expr
import pytest

def test_evaluate_not():
  ctx = mxklabs.expr.ExprContext()

  a = ctx.bool.variable(name="a")
  expr = ctx.bool.logical_not(a)

  assert(True == ctx.evaluate(expr, {a : False}))
  assert(False == ctx.evaluate(expr, {a : True}))

def test_evaluate_and():
  ctx = mxklabs.expr.ExprContext()

  a = ctx.bool.variable(name="a")
  b = ctx.bool.variable(name="b")
  expr = ctx.bool.logical_and(a, b)

  assert(False == ctx.evaluate(expr, {a : False, b : False}))
  assert(False == ctx.evaluate(expr, {a : False, b : True}))
  assert(False == ctx.evaluate(expr, {a : True, b : False}))
  assert(True == ctx.evaluate(expr, {a : True, b : True}))

def test_evaluate_or():
  ctx = mxklabs.expr.ExprContext()

  a = ctx.bool.variable(name="a")
  b = ctx.bool.variable(name="b")
  expr = ctx.bool.logical_or(a, b)

  assert(False == ctx.evaluate(expr, {a : False, b : False}))
  assert(True == ctx.evaluate(expr, {a : False, b : True}))
  assert(True == ctx.evaluate(expr, {a : True, b : False}))
  assert(True == ctx.evaluate(expr, {a : True, b : True}))

def test_expr_hash():
  ctx = mxklabs.expr.ExprContext()

  a1 = ctx.bool.variable(name="a")
  b1 = ctx.bool.variable(name="b")
  not1 = ctx.bool.logical_not(a1)
  not2 = ctx.bool.logical_not(a1)
  and1 = ctx.bool.logical_and(a1, b1)
  and2 = ctx.bool.logical_and(a1, b1)
  or1 = ctx.bool.logical_or(a1, b1)
  or2 = ctx.bool.logical_or(a1, b1)

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
  a1 = ctx.bool.variable(name="a")
  not1 = ctx.bool.logical_not(a1)
  not2 = ctx.bool.logical_not(a1)
  assert(id(a1) != id(not2))
  assert(id(not1) == id(not2))

def test_expr_transform():
  ctx1 = mxklabs.expr.ExprContext(load_defaults=False)
  ctx1.load_expr_class_set("mxklabs.expr.exprset.bool")

  a = ctx1.bool.variable(name="a")
  b = ctx1.bool.variable(name="b")
  expr = ctx1.bool.logical_or(a, b)

  ctx2 = mxklabs.expr.ExprContext(load_defaults=False)
  ctx2.load_expr_class_set("mxklabs.expr.exprset.cnf")

  #ctx_mapping = ctx1.map_onto(ctx2)

def test_logical_not_simplify():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.bool.variable(name="a")
  not_a = ctx.bool.logical_not(a)
  b = ctx.bool.variable(name="b")
  not_b = ctx.bool.logical_not(b)
  t = ctx.bool.constant(value=True)
  f = ctx.bool.constant(value=False)

  # not(True) => False
  assert(f == ctx.bool.logical_not(t))

  # not(False) => True
  assert(t == ctx.bool.logical_not(f))

  # not(not(a)) => a
  assert(a == ctx.bool.logical_not(ctx.bool.logical_not(a)))

  # not(and(a, not(b))) => or(not(a),b))
  expr1 = ctx.bool.logical_not(ctx.bool.logical_and(a, not_b))
  expr2 = ctx.bool.logical_or(not_a, b)
  assert(expr1 == expr2)

  # not(or(a, not(b))) => and(not(a),b)
  expr1 = ctx.bool.logical_not(ctx.bool.logical_or(a, not_b))
  expr2 = ctx.bool.logical_and(not_a, b)
  assert(expr1 == expr2)


ctx = mxklabs.expr.ExprContext()
a1 = ctx.bool.variable(name="a")
not1 = ctx.bool.logical_not(a1)
not2 = ctx.bool.logical_not(a1)
assert(id(a1) != id(not2))
assert(id(not1) == id(not2))

