from ...exprdefset_ import ExprDefSet
from .util_index import UtilIndex
from .util_equal import UtilEqual

class UtilExprDefSet(ExprDefSet):

  def __init__(self, ctx):
    ExprDefSet.__init__(self, ctx, baseid='util', package='mxklabs.expr.exprdefset')
    self._expr_defs = [
      UtilIndex(ctx=ctx, expr_def_set=self),
      UtilEqual(ctx=ctx, expr_def_set=self)
    ]

  def expr_defs(self):
    return self._expr_defs

  def valtype_ids(self):
    return ["mxklabs.expr.valtype.bool",
            "mxklabs.expr.valtype.bitvector"]

  def expr_def_set_ids(self):
    return ["mxklabs.expr.exprdefset.logical",
            "mxklabs.expr.exprdefset.bitvector"]

  def targets(self):
    return []
