from ...exprdefset_ import ExprDefSet
from .logical_and import LogicalAnd
from .logical_not import LogicalNot
from .logical_or import LogicalOr

class LogicalExprDefSet(ExprDefSet):

  def __init__(self, ctx):
    ExprDefSet.__init__(self, ctx, baseid='logical', package='mxklabs.expr.exprdefset')
    self._expr_defs = [
      LogicalAnd(ctx=ctx, expr_def_set=self),
      LogicalNot(ctx=ctx, expr_def_set=self),
      LogicalOr(ctx=ctx, expr_def_set=self)
    ]

  def expr_defs(self):
    return self._expr_defs

  def valtype_ids(self):
    return ["mxklabs.expr.valtype.bool"]

  def targets(self):
    return []
