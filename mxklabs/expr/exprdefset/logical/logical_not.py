from .exprdef import LogicalExprDef
from ...cnftarget import CnfTarget
from ...exprutils import ExprUtils

class LogicalNot(LogicalExprDef):

  def __init__(self, **kwargs):
    LogicalExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting one or more operands, all boolean, no attributes.
    ExprUtils.basic_ops_check(self.id(), 1, 1, self._ctx.valtype.bool(), ops)
    ExprUtils.basic_attrs_check(self.id(), [], attrs)

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bool()

  def evaluate(self, expr, op_values):
    return not op_values[0]

  def simplify(self, ops, attrs):
    op0 = ops[0]

    # not(1) => 0
    # not(0) => 1
    if self._ctx.is_constant(op0):
      return self._ctx.constant(value=not op0.value, valtype=self._ctx.valtype.bool())

    # not(not(e)) => e
    if self._ctx.expr.is_logical_not(op0):
      return op0.ops[0]

    # not(and(e_0,...,e_n)) => or(not(e_0),...,not(e_n)))
    if self._ctx.expr.is_logical_and(op0):
      return self._ctx.expr.logical_or(*[self._ctx.expr.logical_not(op) for op in op0.ops])

    # not(or(e_0,...,e_n)) => and(not(e_0),...,not(e_n)))
    if self._ctx.expr.is_logical_or(op0):
      return self._ctx.expr.logical_and(*[self._ctx.expr.logical_not(op) for op in op0.ops])

    return None

  def has_feature(self, featurestr):
    if featurestr == 'simplify':
      return True
    elif featurestr == 'cnf':
      return True
    return False

  def cnf(self, expr, op_target_mapping, target):
    oplits = [self._unpack(ol) for ol in op_target_mapping]
    return self._pack(target.make_not(oplits[0]))