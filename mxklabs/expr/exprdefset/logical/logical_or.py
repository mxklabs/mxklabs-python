from .exprdef import LogicalExprDef
from ...cnftarget import CnfTarget
from ...exprutils import ExprUtils

class LogicalOr(LogicalExprDef):

  def __init__(self, **kwargs):
    LogicalExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting one or more operands, all boolean, no attributes.
    ExprUtils.basic_ops_check(self.id(), 1, None, self._ctx.valtype.bool(), ops)
    ExprUtils.basic_attrs_check(self.id(), [], attrs)
    # Require all operands to either be boolean variables or negations of boolean variables.
    for index, op in zip(range(len(ops)), ops):
      if (not (self._ctx.is_variable(op) and self._ctx.valtype.is_bool(op.valtype()))) and \
         (not self._ctx.expr.is_logical_not(op)):
        raise RuntimeError(f"'{self.id()}' operands must be either a boolean variable or a logical negation of a boolean variable (operand {index} is '{op}')")

  def replace(self, ops, attrs):
    return None

  def determine_valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bool()

  def determine_value(self, expr, op_values):
    return any(op_values)

  def map_to_target(self, expr, op_target_mapping, target):

    if isinstance(target, CnfTarget):

      oplits = [self._unpack(ol) for ol in op_target_mapping]

      lit = target.ctx().variable(
          name=ExprUtils.make_variable_name_from_expr(expr),
          valtype=target.ctx().valtype.bool())

      # For each op: lit => oplit
      for oplit in oplits:
        target.ctx().add_constraint(target.ctx().expr.logical_or(
          oplit,
          self._make_not(target.ctx(), lit)))

      # not oplit_0 and ... and not oplit_n => not lit
      target.ctx().add_constraint(target.ctx().expr.logical_or(
          *[oplit for oplit in oplits],
          self._make_not(target.ctx(), lit)))

      return self._pack(lit)

    else:
      raise RuntimeError(f"'{self.id()}' does not support target '{type(target)}'")

