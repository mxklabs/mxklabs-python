import mxklabs.expr
import pytest

def test_load():
  ctx = mxklabs.expr.ExprContext(load_defaults=False)
  ctx.load_valtype('mxklabs.expr.valtype.bitvector')

  # Test we can create a bitvector valtype.
  bv1 = ctx.valtype.bitvector(width=10)
  # Test that the context agrees it's a bitvector.
  assert(ctx.valtype.is_bitvector(bv1))
  # Test that the context agrees it's a bitvector of width 10.
  assert(ctx.valtype.is_bitvector(bv1, width=10))
  # Test that the context agrees it's not a bitvector of width 11.
  assert(not ctx.valtype.is_bitvector(bv1, width=11))
  # Test it's equal to itself.
  assert(bv1 == bv1)
  # Test it's not not unequal to itself.
  assert(not (bv1 != bv1))

  # Test calling with non-Valtype objects results in exception.
  with pytest.raises(RuntimeError, match=r"'is_bitvector' argument \('1'\) is not a mxklabs.expr.Valtype object"):
    assert(not ctx.valtype.is_bitvector(1))
  with pytest.raises(RuntimeError, match=r"'is_bitvector' argument \('False'\) is not a mxklabs.expr.Valtype object"):
    assert(not ctx.valtype.is_bitvector(False))

  # Test if we create another bitvector of the same width it's the same object.
  bv2 = ctx.valtype.bitvector(width=10)
  assert(id(bv1) == id(bv2))

  # Test if we create another bitvector of a different width it's another object.
  bv2 = ctx.valtype.bitvector(width=8)
  assert(id(bv1) != id(bv2))

  # Test __str__ and __repr__.
  assert("bitvector(width=10)" == str(bv1))
  assert("bitvector(width=10)" == repr(bv1))

  # Test a boolean isn't mistaken for a bitvector and vice versa.
  ctx.load_valtype('mxklabs.expr.valtype.bool')
  assert(not ctx.valtype.is_bool(bv1))
  bool1 = ctx.valtype.bool()
  assert(not ctx.valtype.is_bitvector(bool1))


