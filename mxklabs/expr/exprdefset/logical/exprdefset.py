from ...exprdefset_ import ExprDefSet
from .logical_and import LogicalAnd
from .logical_implies import LogicalImplies
from .logical_nand import LogicalNand
from .logical_nor import LogicalNor
from .logical_not import LogicalNot
from .logical_or import LogicalOr
from .logical_xor import LogicalXor
from .logical_xnor import LogicalXnor

class LogicalExprDefSet(ExprDefSet):

  def __init__(self, ctx):
    ExprDefSet.__init__(self, ctx, baseid='logical', package='mxklabs.expr.exprdefset')
    self._expr_defs = [
      LogicalAnd(ctx=ctx, expr_def_set=self),
      LogicalImplies(ctx=ctx, expr_def_set=self),
      LogicalNand(ctx=ctx, expr_def_set=self),
      LogicalNor(ctx=ctx, expr_def_set=self),
      LogicalNot(ctx=ctx, expr_def_set=self),
      LogicalOr(ctx=ctx, expr_def_set=self),
      LogicalXor(ctx=ctx, expr_def_set=self),
      LogicalXnor(ctx=ctx, expr_def_set=self)
    ]

  def expr_defs(self):
    return self._expr_defs

  def valtype_ids(self):
    return ["mxklabs.expr.valtype.bool"]

  def expr_def_set_ids(self):
    return ["mxklabs.expr.exprdefset.util"]

  def targets(self):
    return []
