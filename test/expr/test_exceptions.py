import mxklabs.expr
import pytest

def test_too_few_ops():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.prop.variable(name="a")
  with pytest.raises(RuntimeError, match=r"'prop\.logical_and' expects at least 2 operands \(got 1\)"):
    ctx.prop.logical_and(a)

def test_not_exact_number_of_ops():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.prop.variable(name="a")
  with pytest.raises(RuntimeError, match=r"'prop\.logical_not' expects exactly 1 operand \(got 2\)"):
    ctx.prop.logical_not(a, a)

def test_load_exprset_twice():
  ctx = mxklabs.expr.ExprContext(load_mxklabs_exprsets=False)
  ctx.load_exprset("mxklabs.expr.exprsets.prop")
  with pytest.raises(RuntimeError, match=r"'mxklabs.expr.exprsets.prop' cannot be loaded \(name 'prop' is already in use\)"):
    ctx.load_exprset("mxklabs.expr.exprsets.prop")