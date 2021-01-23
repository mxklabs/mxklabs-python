import mxklabs.expr
import pytest

from exprtester import ExprTester

def test_util_index():
  ctx = mxklabs.expr.ExprContext()

  # Test with a bitvector.
  inputs = [ctx.valtype.bitvector(width=4)]
  output = lambda op0: (op0 >> 3) & 1 == 1
  attrs = {'index':3}
  ExprTester(ctx, ctx.expr.util_index, inputs, attrs, output)

def test_util_equal():
  ctx = mxklabs.expr.ExprContext()

  # Test with a bitvector.
  inputs = [ctx.valtype.bitvector(width=2), ctx.valtype.bitvector(width=2)]
  output = lambda op0, op1: op0 == op1
  attrs = {}
  ExprTester(ctx, ctx.expr.util_equal, inputs, attrs, output)
