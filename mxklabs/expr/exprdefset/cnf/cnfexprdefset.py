from ...exprdefset import ExprDefSet
from .logical_not import LogicalNot
from .logical_or import LogicalOr

class CnfExprDefSet(ExprDefSet):

  def __init__(self, ctx):
    ExprDefSet.__init__(self, ctx, baseid='cnf', package='mxklabs.expr.exprdefset')
    self._expr_defs = [
      LogicalNot(ctx, self),
      LogicalOr(ctx, self)
    ]

  def expr_defs(self):
    return self._expr_defs

  def valtypes(self):
    return ["mxklabs.expr.valtype.bool"]

  def targets(self):
    return []
