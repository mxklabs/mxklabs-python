import mxklabs.expr
import pytest

def test_too_few_ops():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.prop.variable(name="a")
  with pytest.raises(RuntimeError, match=r"'logical_and' expects at least 2 operands \(got 1\)"):
    ctx.prop.logical_and(a)

def test_not_exact_number_of_ops():
  ctx = mxklabs.expr.ExprContext()
  a = ctx.prop.variable(name="a")
  with pytest.raises(RuntimeError, match=r"'logical_not' expects exactly 1 operand \(got 2\)"):
    ctx.prop.logical_not(a, a)

def test_load_exprset_twice():
  ctx = mxklabs.expr.ExprContext(load_default_expr_class_sets=False)
  ctx.load_expr_class_set("mxklabs.expr.definitions.exprclasssets.prop")
  with pytest.raises(RuntimeError, match=r"'mxklabs.expr.definitions.exprclasssets.prop' cannot be loaded \(name 'prop' is already in use\)"):
    ctx.load_expr_class_set("mxklabs.expr.definitions.exprclasssets.prop")