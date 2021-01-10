from ...exprdef import ExprDef

class CnfExprDef(ExprDef):

  def __init__(self, **kwargs):
    ExprDef.__init__(self, **kwargs)

  def _make_not(self, target_ctx, oplit):
    # All literals are either variables or negations of variables. If we
    # are asked to negate a negation, return the variable.
    if target_ctx.cnf.is_logical_not(oplit):
      return oplit.ops[0]
    else:
      return target_ctx.cnf.logical_not(oplit)