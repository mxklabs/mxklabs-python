import mxklabs.expr
import pytest

from exprtester import ExprTester

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

  # Test values.
  bv2 = ctx.valtype.bitvector(width=2)
  bv3 = ctx.valtype.bitvector(width=3)
  bv4 = ctx.valtype.bitvector(width=4)
  assert(list(bv2.values()) == [0,1,2,3])
  assert(list(bv3.values()) == [0,1,2,3,4,5,6,7])
  assert(list(bv4.values()) == [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

def test_bitvector_from_bool():
  ctx = mxklabs.expr.ExprContext()#

  def bool_to_int(boolval):
    return 1 if boolval else 0

  # Test with three bools
  inputs = [ctx.valtype.bool(), ctx.valtype.bool(), ctx.valtype.bool()]
  output = lambda op0, op1, op2: bool_to_int(op0) + (bool_to_int(op1) << 1) + (bool_to_int(op2) << 2)
  attrs = {'width':3}
  ExprTester(ctx, ctx.expr.bitvector_from_bool, inputs, attrs, output)

def test_bitvector_mult():
  ctx = mxklabs.expr.ExprContext()#

  # Test with two 3-bit bitvectors
  inputs = [ctx.valtype.bitvector(width=3), ctx.valtype.bitvector(width=3)]
  output = lambda op0, op1: op0 * op1
  attrs = {'width':6}
  ExprTester(ctx, ctx.expr.bitvector_mult, inputs, attrs, output)

