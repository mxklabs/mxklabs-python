from ...exprdef import ExprDef

class LogicalExprDef(ExprDef):

  def __init__(self, **kwargs):
    ExprDef.__init__(self, **kwargs)

  def _pack(self, lit):
    return [lit]

  def _unpack(self, booltup):
    return booltup[0]

  def _make_not(self, target_ctx, oplit):
    # All literals are either variables or negations of variables. If we
    # are asked to negate a negation, return the variable.
    if target_ctx.expr.is_logical_not(oplit):
      return oplit.ops[0]
    else:
      return target_ctx.expr.logical_not(oplit)