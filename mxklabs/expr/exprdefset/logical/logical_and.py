from .exprdef import LogicalExprDef
from ...cnftarget import CnfTarget
from ...exprutils import ExprUtils

class LogicalAnd(LogicalExprDef):

  def __init__(self, **kwargs):
    LogicalExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting one or more operands, all boolean, no attributes.
    ExprUtils.basic_ops_check(self.id(), 1, None, self._ctx.valtype.bool(), ops)
    ExprUtils.basic_attrs_check(self.id(), [], attrs)

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bool()

  def evaluate(self, expr, op_values):
    return any(op_values)

  def has_feature(self, featurestr):
    if featurestr == 'simplify':
      return True
    elif featurestr == 'cnf':
      return True
    return False

  def simplify(self, ops, attrs):
    # and(..., 0, ...) => 0
    if any([self._ctx.is_constant(op) and not op.value() for op in ops]):
      return self._ctx.constant(value=False, valtype=self._ctx.valtype.bool())

    # and(1, ..., 1) => 1
    if all([self._ctx.is_constant(op) and op.value() for op in ops]):
      return self._ctx.constant(value=True, valtype=self._ctx.valtype.bool())

    # TODO: if and(expr, ..., not expr) => 0

    # Sort by operand hash.
    ops = list(ops)
    new_ops = sorted(ops, key=hash)
    if new_ops != ops:
      return self._ctx.expr.logical_and(*new_ops)

    return None

  def cnf(self, expr, op_target_mapping, target):
    oplits = [self._unpack(ol) for ol in op_target_mapping]

    lit = target.make_lit(expr)

    # For each op: lit => oplit
    for oplit in oplits:
      target.ctx().add_constraint(target.ctx().expr.logical_or(
        oplit,
        target.make_not(lit)))

    # oplit_0 and ... and oplit_n => lit
    target.ctx().add_constraint(target.ctx().expr.logical_or(
        *[target.make_not(oplit) for oplit in oplits],
        lit))

    return self._pack(lit)