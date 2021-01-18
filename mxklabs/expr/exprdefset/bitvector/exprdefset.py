from ...exprdefset_ import ExprDefSet
from .bitvector_from_bool import BitvectorFromBool
from .bitvector_to_bool import BitvectorToBool

class BitvectorExprDefSet(ExprDefSet):

  def __init__(self, ctx):
    ExprDefSet.__init__(self, ctx, baseid='bitvector', package='mxklabs.expr.exprdefset')
    self._expr_defs = [
      BitvectorFromBool(ctx=ctx, expr_def_set=self),
      BitvectorToBool(ctx=ctx, expr_def_set=self)
    ]

  def expr_defs(self):
    return self._expr_defs

  def valtype_ids(self):
    return ["mxklabs.expr.valtype.bool",
            "mxklabs.expr.valtype.bitvector"]

  def targets(self):
    return []
