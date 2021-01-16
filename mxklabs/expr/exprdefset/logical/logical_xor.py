from .exprdef import LogicalExprDef
from ...cnftarget import CnfTarget
from ...exprutils import ExprUtils

class LogicalXor(LogicalExprDef):

  def __init__(self, **kwargs):
    LogicalExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting two operands, all boolean, no attributes.
    ExprUtils.basic_ops_check(self.id(), 2, 2, self._ctx.valtype.bool(), ops)
    ExprUtils.basic_attrs_check(self.id(), [], attrs)

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bool()

  def evaluate(self, expr, op_values):
    return any(op_values)

  def simplify(self, ops, attrs):
    op0 = ops[0]
    op1 = ops[1]

    # xor(const0,const1) => const0 ^ const1
    if self._ctx.is_constant(op0) and self._ctx.is_constant(op1):
      return self._ctx.constant(value=op0.value()!=op1.value(), valtype=self._ctx.valtype.bool())

    # Sort by operand hash.
    if hash(op1) < hash(op0):
      return self._ctx.expr.logical_xor(op1, op0)

    return None

  def has_feature(self, featurestr):
    if featurestr == 'simplify':
      return True
    elif featurestr == 'cnf':
      return True
    return False

  def cnf(self, expr, op_target_mapping, target):
    oplits = [self._unpack(ol) for ol in op_target_mapping]
    oplit0 = oplits[0]
    oplit1 = oplits[1]

    lit = target.make_lit(expr)

    # oplit0 and not oplit1 => lit
    target.ctx().add_constraint(target.ctx().expr.logical_or(
        target.make_not(oplit0),
        oplit1,
        lit))

    # not oplit0 and oplit1 => lit
    target.ctx().add_constraint(target.ctx().expr.logical_or(
        oplit0,
        target.make_not(oplit1),
        lit))

    # oplit0 and oplit1 => not lit
    target.ctx().add_constraint(target.ctx().expr.logical_or(
        target.make_not(oplit0),
        target.make_not(oplit1),
        target.make_not(lit)))

    # not oplit0 and not oplit1 => not lit
    target.ctx().add_constraint(target.ctx().expr.logical_or(
        oplit0,
        oplit1,
        target.make_not(lit)))

    return self._pack(lit)
