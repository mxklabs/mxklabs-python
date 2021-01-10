import mxklabs.expr
import pytest

def test_cnf():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bool')
  ctx.load_expr_def_set('mxklabs.expr.exprdefset.cnf')

  # Test we can create a boolean constant.
  v1 = ctx.variable(name='v1', valtype=ctx.valtype.bool())
  v2 = ctx.variable(name='v2', valtype=ctx.valtype.bool())

  # Create logical_or(v1, logical_not(v2))
  expr = ctx.cnf.logical_or(
    v1,
    ctx.cnf.logical_not(v2))

  # Add constraint.
  ctx.add_constraint(expr)

def test_invalid_exprs():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bool')
  ctx.load_expr_def_set('mxklabs.expr.exprdefset.cnf')

  # Test we can create a boolean constant.
  false = ctx.constant(value=True, valtype=ctx.valtype.bool())
  v1 = ctx.variable(name='v1', valtype=ctx.valtype.bool())

  # logical_or with constant.
  with pytest.raises(RuntimeError, match=r"'mxklabs.expr.exprdefset.cnf.logical_or' operands must be either a boolean variable or a logical negation of a boolean variable \(operand 0 is '1'\)"):
    ctx.cnf.logical_or(false)

  # logical_or with logical_or.
  with pytest.raises(RuntimeError, match=r"'mxklabs.expr.exprdefset.cnf.logical_or' operands must be either a boolean variable or a logical negation of a boolean variable \(operand 0 is 'mxklabs.expr.exprdefset.cnf.logical_or\(v1\)'\)"):
    ctx.cnf.logical_or(ctx.cnf.logical_or(v1))

  # logical_not with constant
  with pytest.raises(RuntimeError, match=r"'mxklabs.expr.exprdefset.cnf.logical_not' operand must be a boolean variable \(operand is '1'\)"):
    ctx.cnf.logical_not(false)

  # logical_not with logical_or
  with pytest.raises(RuntimeError, match=r"'mxklabs.expr.exprdefset.cnf.logical_not' operand must be a boolean variable \(operand is 'mxklabs.expr.exprdefset.cnf.logical_or\(v1\)'\)"):
    ctx.cnf.logical_not(ctx.cnf.logical_or(v1))

  # logical_not with logical_not
  with pytest.raises(RuntimeError, match=r"'mxklabs.expr.exprdefset.cnf.logical_not' operand must be a boolean variable \(operand is 'mxklabs.expr.exprdefset.cnf.logical_not\(v1\)'\)"):
    ctx.cnf.logical_not(ctx.cnf.logical_not(v1))
