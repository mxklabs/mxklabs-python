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

  def false(self):
    return self._false