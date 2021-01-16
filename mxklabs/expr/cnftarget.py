from .exprutils import ExprUtils

class CnfTarget:

  def __init__(self, ctx):
    self._ctx = ctx
    self._true = self._ctx.variable(name='__true', valtype=self._ctx.valtype.bool())
    self._ctx.add_constraint(self._ctx.expr.logical_or(self._true))
    self._false = self._ctx.expr.logical_not(self._true)

  def ctx(self):
    return self._ctx

  def true(self):
    return self._true

  def make_lit(self, expr, bit=None):
    return self._ctx.variable(
        name=ExprUtils.make_variable_name_from_expr(expr, bit),
        valtype=self._ctx.valtype.bool())

  def make_not(self, lit):
    # All literals are either variables or negations of variables. If we
    # are asked to negate a negation, return the variable.
    if self._ctx.expr.is_logical_not(lit):
      return lit.ops()[0]
    else:
      return self._ctx.expr.logical_not(lit)

  def false(self):
    return self._false