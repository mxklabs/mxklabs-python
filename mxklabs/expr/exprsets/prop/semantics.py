class Semantics:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, expr, op_value):
    return not op_value

  def logical_and(self, expr, *op_values):
    return all(op_values)

  def logical_nand(self, expr, *op_values):
    return not(all(op_values))

  def logical_or(self, expr, *op_values):
    return any(op_values)

  def logical_nor(self, expr, *op_values):
    return not(any(op_values))

  def logical_xor(self, expr, op_value0, op_value1):
    return op_value0 != op_value1

  def logical_xnor(self, expr,  op_value0, op_value1):
    return op_value0 == op_value1

  def implies(self, expr, op_value0, op_value1):
    return op_value1 or not op_value0