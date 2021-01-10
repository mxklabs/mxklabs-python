import mxklabs.expr
import pytest

def test_too_few_ops():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.bool.variable(name="a")
  with pytest.raises(RuntimeError, match=r"'logical_and' expects at least 2 operands \(got 1\)"):
    ctx.bool.logical_and(a)

def test_not_exact_number_of_ops():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.bool.variable(name="a")
  with pytest.raises(RuntimeError, match=r"'logical_not' expects exactly 1 operand \(got 2\)"):
    ctx.bool.logical_not(a, a)

def test_load_exprset_twice():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_expr_class_set("mxklabs.expr.exprset.bool")
  with pytest.raises(RuntimeError, match=r"'mxklabs.expr.exprset.bool' cannot be loaded twice \(already loaded\)"):
    ctx.load_expr_class_set("mxklabs.expr.exprset.bool")