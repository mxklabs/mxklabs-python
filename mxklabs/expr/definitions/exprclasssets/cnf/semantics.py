from ....exprutils import ExprUtils

class InputValidator:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_not', 1, 1, self.ctx.bool(), ops, [], attrs)

  def logical_or(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_not', 2, 0, self.ctx.bool(), ops, [], attrs)

class TypeInference:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, op_valtype, **attrs):
    return self.ctx.bool()

  def logical_or(self, *op_valt_types, **attrs):
    return self.ctx.bool()

class ValueInference:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, expr, op_value):
    return not op_value

  def logical_or(self, expr, *op_values):
    return any(op_values)

"""
class LogicalNot(ExprClass):
  def __init__(self):
    ExprClass.__init__(self, min_ops=1, max_ops=1, attrs=[])

  def check_ops(self, op0):
    pass

  def do_valtype_inference(self, op0):
    pass

  def do_constant_propagation(self, op0):
    if op0.is_constant():
      evaluate(op0.value)

  def evaluate(self, op0_value):
    pass
"""


