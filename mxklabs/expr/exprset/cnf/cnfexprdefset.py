from ...exprdefset import ExprDefSet
from .logical_not import LogicalNot
from .logical_or import LogicalOr

class CnfExprDefSet(ExprDefSet):

  def __init__(self, ctx):
    ExprDefSet.__init__(self, ctx)
    self._expr_defs = [
      LogicalNot(ctx),
      LogicalOr(ctx)
    ]

  def get_namespace(self):
    return "cnf"

  def get_expr_defs(self):
    return self._expr_defs

  def get_valtypes(self):
    return [
      "mxklabs.expr.valtype.bool"
    ]

  def get_targets(self):
    return []
