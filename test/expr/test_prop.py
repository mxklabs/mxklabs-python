import mxklabs.expr
import pytest

def test_evaluate_and():
  ctx = mxklabs.expr.ExprContext()


  a = ctx.prop.variable(name="a")
  b = ctx.prop.variable(name="b")
  c = ctx.prop.logical_and(a, b)

  assert(False == c.evaluate({a : False, b : False}))
  assert(False == c.evaluate({a : False, b : True}))
  assert(False == c.evaluate({a : True, b : False}))
  assert(True == c.evaluate({a : True, b : True}))
