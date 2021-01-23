from .exprdef import UtilExprDef
from ...exprutils import ExprUtils

class UtilEqual(UtilExprDef):

  def __init__(self, **kwargs):
    UtilExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    ExprUtils.basic_attrs_check(self.id(), {}, attrs)
    ExprUtils.basic_ops_check(self.id(), 2, 2, None, ops)

    if (ops[0].valtype() != ops[1].valtype()):
      raise RuntimeError(f"'{self.id()}' expected operands to have the same valtype (got {ops[0].valtype()} and {ops[1].valtype()})")

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bool()

  def evaluate(self, expr, op_values):
    return (op_values[0] == op_values[1])

  def has_feature(self, featurestr):
    if featurestr == 'decompose':
      return True
    if featurestr == 'simplify':
      return True
    return False

  def decompose(self, expr):
    op_valtype = expr.ops()[0].valtype()

    # For bools, it's basically xnor.
    if self._ctx.valtype.is_bool(op_valtype):
      return self._ctx.expr.logical_xnor(*expr.ops())

    # For bitvectors, it's an logical_and over an bit-wise logical-xnor.
    if self._ctx.valtype.is_bitvector(op_valtype):
      width = op_valtype.attrs()['width']
      ops = []
      for bit in range(width):
        ops.append(self._ctx.expr.logical_xnor(
          self._ctx.expr.util_index(expr.ops()[0], index=bit),
          self._ctx.expr.util_index(expr.ops()[1], index=bit)))
      return self._ctx.expr.logical_and(*ops)

    # Can't simplify.
    return expr

  def simplify(self, expr):
    op_valtype = expr.ops()[0].valtype()

    # util_equals(const0, const1) => const0 == const1
    if self._ctx.is_constant(expr.ops()[0]) and self._ctx.is_constant(expr.ops[1]):
      return self._ctx.constant(value=expr.ops()[0].value() == expr.ops()[1].value(), valtype=self._ctx.valtype.bool())

    # For bools, if one side if true, substitute for other side.
    for side in [0, 1]:
      if self._ctx.is_constant(expr.ops()[side]) and self._ctx.valtype.is_bool(op_valtype):
        if expr.ops()[side].value():
          return expr.ops()[1 - side]
        else:
          return self._ctx.expr.logical_not(expr.ops()[1 - side])

    # Can't simplify.
    return expr


