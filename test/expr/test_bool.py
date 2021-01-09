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

  # Test other things are not considered bools.
  assert(not ctx.valtype.is_bool(1))
  assert(not ctx.valtype.is_bool(False))

  # Test if we create another bool it's the same object.
  bool2 = ctx.valtype.bool()
  assert(id(bool1) == id(bool2))

