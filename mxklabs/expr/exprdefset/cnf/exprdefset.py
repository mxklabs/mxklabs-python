from ...exprdefset_ import ExprDefSet
from .logical_not import LogicalNot
from .logical_or import LogicalOr

class CnfExprDefSet(ExprDefSet):

  def __init__(self, ctx):
    ExprDefSet.__init__(self, ctx, baseid='cnf', package='mxklabs.expr.exprdefset')
    self._expr_defs = [
      LogicalNot(ctx=ctx, expr_def_set=self),
      LogicalOr(ctx=ctx, expr_def_set=self)
    ]

  def expr_defs(self):
    return self._expr_defs

  def valtype_ids(self):
    return ["mxklabs.expr.valtype.bool"]

  def expr_def_set_ids(self):
    return []

  def targets(self):
    return []
