from ...exprdefset_ import ExprDefSet
from .bitvector_from_bool import BitvectorFromBool
from .bitvector_mult import BitvectorMult

class BitvectorExprDefSet(ExprDefSet):

  def __init__(self, ctx):
    ExprDefSet.__init__(self, ctx, baseid='bitvector', package='mxklabs.expr.exprdefset')
    self._expr_defs = [
      BitvectorFromBool(ctx=ctx, expr_def_set=self),
      BitvectorMult(ctx=ctx, expr_def_set=self)
    ]

  def expr_defs(self):
    return self._expr_defs

  def valtype_ids(self):
    return ["mxklabs.expr.valtype.bool",
            "mxklabs.expr.valtype.bitvector"]

  def expr_def_set_ids(self):
    return ["mxklabs.expr.exprdefset.logical",
            "mxklabs.expr.exprdefset.util"]

  def targets(self):
    return []
