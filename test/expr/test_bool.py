import mxklabs.expr
import pytest

def test_load():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bool')

  # Test we can create a boolean valtype.
  bool1 = ctx.valtype.bool()
  # Test that the context agrees it's a bool.
  assert(ctx.valtype.is_bool(bool1))
  # Test it's equal to itself.
  assert(bool1 == bool1)
  # Test it's not not unequal to itself.
  assert(not (bool1 != bool1))

  # Test calling with non-Valtype objects results in exception.
  with pytest.raises(RuntimeError, match=r"'is_bool' argument \('1'\) is not a mxklabs.expr.Valtype object"):
    assert(not ctx.valtype.is_bool(1))
  with pytest.raises(RuntimeError, match=r"'is_bool' argument \('False'\) is not a mxklabs.expr.Valtype object"):
    assert(not ctx.valtype.is_bool(False))

  # Test if we create another bool it's the same object.
  bool2 = ctx.valtype.bool()
  assert(id(bool1) == id(bool2))

  # Test __str__ and __repr__.
  assert("bool" == str(bool1))
  assert("bool" == repr(bool1))

  # Test values.
  assert(list(bool1.values()) == [False, True])

