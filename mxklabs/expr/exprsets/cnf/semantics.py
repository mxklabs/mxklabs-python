class Semantics:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, expr, op_value):
    return not op_value

  def logical_and(self, expr, *op_values):
    return all(op_values)

  def logical_or(self, expr, *op_values):
    return any(op_values)