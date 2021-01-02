from ...exprutils import ExprUtils

class InputValidator:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_not', 1, 1, self.ctx.valtypes.bool(), ops, [], attrs)
    if not self.ctx.is_variable(ops[0]) or ops[0].valtype != self.ctx.valtypes.bool():
      raise RuntimeError(f"'logical_not' must negate a variable (got operand '{ops[0].identifier}')")

  def logical_or(self, *ops, **attrs):
    ExprUtils.basicOpsAndAttrsCheck('logical_or', 1, None, self.ctx.valtypes.bool(), ops, [], attrs)
    for op in ops:
      if not self.ctx.is_variable(op) and not self.ctx.cnf.is_logical_not(op):
        raise RuntimeError(f"'logical_or' must be a disjunction over 'variable' and 'logical_not' expression (got operand '{op.identifier}')")

class ExprSimplifier:
  """ Responsible for simplifying and canonicalising expressions. Return
      an expression object to replace the about-to-be-constructed expression
      to replace it with something simpler. Take care not to create infinite
      recursion. Return None to construct the expression as-is.
  """
  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, op0, **attrs):
    return None

  def logical_or(self, *ops, **attrs):
    return None

class TypeInference:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, op0, **attrs):
    return self.ctx.valtypes.bool()

  def logical_or(self, *ops, **attrs):
    return self.ctx.valtypes.bool()

class ValueInference:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, expr, op_value):
    return not op_value

  def logical_or(self, expr, *op_values):
    return any(op_values)

class CnfMapping:

  def __init__(self, ctx):
    self.ctx = ctx

  def logical_not(self, expr, oplit):
    return self._make_not(oplit)

  def logical_or(self, expr, *oplits):
    lit = self.ctx.make_var(f'{expr}', self.ctx.valtypes.bool)

    # For each op: lit => oplit
    for oplit in oplits:
      self.ctx.add_constraint(self.ctx.cnf.logical_or(
        oplit,
        self._make_not(lit)))

    # not oplit_0 and ... and not oplit_n => not lit
    self.ctx.add_constraint(self.ctx.cnf.logical_or(
        *[oplit for oplit in oplits],
        self._make_not(lit)))

    return lit

  def _make_not(self, oplit):
    if self.ctx.cnf.is_logical_not(oplit):
      return oplit.ops[0]
    else:
      return self.ctx.cnf.logical_not(oplit)



