import mxklabs.expr
import pytest

def test_variable():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bool')

  # Test we can create a boolean variable.
  bool1 = ctx.variable(name='bool1', valtype=ctx.valtype.bool())

def test_invalid_valtype():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bool')

  # Check we can't use some random object for valtype.
  with pytest.raises(RuntimeError, match=r"valtype argument of variable 'bool1' \('1'\) is not a mxklabs.expr.Valtype object"):
    bool1 = ctx.variable(name='bool1', valtype=1)

def test_invalid_name():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bool')

  # Check we can't use some random object for name.
  with pytest.raises(RuntimeError, match=r"name argument of variable is not a 'str'"):
    bool1 = ctx.variable(name=1, valtype=ctx.valtype.bool())

def test_valtype_from_different_ctx():
  ctx1 = mxklabs.expr.ExprContext(load_defaults=False)
  ctx1.load_valtype('mxklabs.expr.valtype.bool')

  ctx2 = mxklabs.expr.ExprContext(load_defaults=False)
  ctx2.load_valtype('mxklabs.expr.valtype.bool')

  # Check we can't create a variable in ctx1 with valtype from ctx2.
  with pytest.raises(RuntimeError, match=r"valtype argument of variable 'bool1' \('bool'\) was created in a different context"):
    bool1 = ctx1.variable(name='bool1', valtype=ctx2.valtype.bool())

def test_duplicate_variable_name_in_ctx():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bool')

  bool1 = ctx.variable(name='bool1', valtype=ctx.valtype.bool())

  # Check we can't use the same name twice.
  with pytest.raises(RuntimeError, match=r"variable with name 'bool1' already exists in context"):
    bool2 = ctx.variable(name='bool1', valtype=ctx.valtype.bool())

  # Check we can use a different name.
  bool2 = ctx.variable(name='bool2', valtype=ctx.valtype.bool())
