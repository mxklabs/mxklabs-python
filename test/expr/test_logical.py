import mxklabs.expr

from exprtester import ExprTester

def test_logical_and():
  ctx = mxklabs.expr.ExprContext()

  # Test with one input.
  inputs = [ctx.valtype.bool()]
  output = lambda op0: op0
  ExprTester(ctx, ctx.expr.logical_and, inputs, {}, output)

  # Test with two inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1: op0 and op1
  ExprTester(ctx, ctx.expr.logical_and, inputs, {}, output)

  # Test with three inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1, op2: op0 and op1 and op2
  ExprTester(ctx, ctx.expr.logical_and, inputs, {}, output)

def test_logical_implies():
  ctx = mxklabs.expr.ExprContext()

  # Test with two inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1: not op0 or op1
  ExprTester(ctx, ctx.expr.logical_implies, inputs, {}, output)

def test_logical_nand():
  ctx = mxklabs.expr.ExprContext()

  # Test with one input.
  inputs = [ctx.valtype.bool()]
  output = lambda op0: not op0
  ExprTester(ctx, ctx.expr.logical_nand, inputs, {}, output)

  # Test with two inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1: not (op0 and op1)
  ExprTester(ctx, ctx.expr.logical_nand, inputs, {}, output)

  # Test with three inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1, op2: not (op0 and op1 and op2)
  ExprTester(ctx, ctx.expr.logical_nand, inputs, {}, output)

def test_logical_nor():
  ctx = mxklabs.expr.ExprContext()

  # Test with one input.
  inputs = [ctx.valtype.bool()]
  output = lambda op0: not op0
  ExprTester(ctx, ctx.expr.logical_nor, inputs, {}, output)

  # Test with two inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1: not (op0 or op1)
  ExprTester(ctx, ctx.expr.logical_nor, inputs, {}, output)

  # Test with three inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1, op2: not (op0 or op1 or op2)
  ExprTester(ctx, ctx.expr.logical_nor, inputs, {}, output)

def test_logical_not():
  ctx = mxklabs.expr.ExprContext()

  # Test with one input.
  inputs = [ctx.valtype.bool()]
  output = lambda op0: not op0
  ExprTester(ctx, ctx.expr.logical_not, inputs, {}, output)

def test_logical_or():
  ctx = mxklabs.expr.ExprContext()

  # Test with one input.
  inputs = [ctx.valtype.bool()]
  output = lambda op0: op0
  ExprTester(ctx, ctx.expr.logical_or, inputs, {}, output)

  # Test with two inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1: op0 or op1
  ExprTester(ctx, ctx.expr.logical_or, inputs, {}, output)

  # Test with three inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1, op2: op0 or op1 or op2
  ExprTester(ctx, ctx.expr.logical_or, inputs, {}, output)

def test_logical_xnor():
  ctx = mxklabs.expr.ExprContext()

  # Test with two inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1: op0 == op1
  ExprTester(ctx, ctx.expr.logical_xnor, inputs, {}, output)

def test_logical_xor():
  ctx = mxklabs.expr.ExprContext()

  # Test with two inputs.
  inputs = [ctx.valtype.bool(),ctx.valtype.bool()]
  output = lambda op0, op1: op0 != op1
  ExprTester(ctx, ctx.expr.logical_xor, inputs, {}, output)