import mxklabs.expr
import pytest

def test_cnf():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bool')
  ctx.load_expr_def_set('mxklabs.expr.exprdefset.cnf')

  # Test we can create a boolean constant.
  true = ctx.constant(value=True, valtype=ctx.valtype.bool())
  false = ctx.constant(value=True, valtype=ctx.valtype.bool())

  v1 = ctx.variable(name='v1', valtype=ctx.valtype.bool())
  v2 = ctx.variable(name='v2', valtype=ctx.valtype.bool())
  v2 = ctx.variable(name='v3', valtype=ctx.valtype.bool())

  # Expr.
  ctx.add_constraint(
    ctx.cnf.logical_or(
      v1,
      ctx.cnf.logical_not(v2),
      false
    ))


  # Check you can't add variables as constraints.
  # Check you can't add nots as constraints constraints.

  # Check you can't have nots in nots.
  # Check you can't have constants in nots.
  # Check you can't have ors in nots.

  # Check you can't have ors in ors.
  # Check you can't have constants in ors.