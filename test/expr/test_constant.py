import mxklabs.expr
import pytest

def test_constant():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bool')

  # Test we can create a boolean constant.
  bool1 = ctx.constant(value=True, valtype=ctx.valtype.bool())
  bool2 = ctx.constant(value=False, valtype=ctx.valtype.bool())

  # Check we can also create them with 0, 1.
  bool3 = ctx.constant(value=1, valtype=ctx.valtype.bool())
  bool4 = ctx.constant(value=0, valtype=ctx.valtype.bool())

  # Check object equivalences.
  assert(id(bool1) != id(bool2))
  assert(id(bool1) == id(bool3))
  assert(id(bool1) != id(bool4))
  assert(id(bool2) == id(bool4))

def test_invalid_value():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bool')

  # Check we can't use some random object for value.
  with pytest.raises(RuntimeError, match=r"'3' is not a valid value for valtype 'bool'"):
    bool1 = ctx.constant(value=3, valtype=ctx.valtype.bool())

def test_valtype_from_different_ctx():
  ctx1 = mxklabs.expr.ExprContext(load_defaults=False)
  ctx1.load_valtype('mxklabs.expr.valtype.bool')

  ctx2 = mxklabs.expr.ExprContext(load_defaults=False)
  ctx2.load_valtype('mxklabs.expr.valtype.bool')

  # Check we can't create a variable in ctx1 with valtype from ctx2.
  with pytest.raises(RuntimeError, match=r"valtype argument of constant \('bool'\) was created in a different context"):
    bool1 = ctx1.constant(value='bool1', valtype=ctx2.valtype.bool())
