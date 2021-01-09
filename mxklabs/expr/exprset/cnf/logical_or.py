from .cnfexprdef import CnfExprDef
from ...exprutils import ExprUtils

class LogicalOr(CnfExprDef):

  def __init__(self, **kwargs):
    CnfExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting one or more operands, all boolean, no attributes.
    ExprUtils.basic_ops_and_attrs_check(self.id(), 1, None, self._ctx.bool(), ops, [], attrs)
    # Require all operands to either be boolean variables or negations of boolean variables.
    for op in ops:
      if (not self._ctx.is_variable(ops[0]) or ops[0].valtype() != self._ctx.bool()) and \
         (not self._ctx.cnf.is_logical_not(op))
        raise RuntimeError(f"'{self.id()}' must be a disjunction over 'variable' and 'logical_not' expression (got '{op}')")

  def validate_constraint(self, expr):
    return None

  def replace(self, ops, attrs):
    return None

  def determine_valtype(self, ops, attrs, op_valtypes):
    return self._ctx.bool()

  def determine_value(self, expr, op_values):
    return any(op_values)

  def map_to_target(self, expr, op_target_mapping, target_ctx):

    # TODO: Check target is cnf.

    lit = target_ctx.bool.variable(name=
        ExprUtils.make_variable_name_from_expr(expr)

    # For each op: lit => oplit
    for oplit in op_target_mapping:
      target_ctx.add_constraint(target_ctx.cnf.logical_or(
        oplit,
        make_not(target_ctx, lit)))

    # not oplit_0 and ... and not oplit_n => not lit
    target_ctx.add_constraint(target_ctx.cnf.logical_or(
        *[oplit for oplit in op_target_mapping],
        make_not(target_ctx, lit)))

    return lit
