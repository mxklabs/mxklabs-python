from .cnfexprdef import CnfExprDef
from ...exprutils import ExprUtils

class LogicalOr(CnfExprDef):

  def __init__(self, **kwargs):
    CnfExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting one or more operands, all boolean, no attributes.
    ExprUtils.basic_ops_check(self.id(), 1, None, self._ctx.valtype.bool(), ops)
    ExprUtils.basic_attrs_check(self.id(), [], attrs)
    # Require all operands to either be boolean variables or negations of boolean variables.
    for index, op in zip(range(len(ops)), ops):
      if (not (self._ctx.is_variable(op) and self._ctx.valtype.is_bool(op.valtype()))) and \
         (not self._ctx.cnf.is_logical_not(op)):
        raise RuntimeError(f"'{self.id()}' operands must be either a boolean variable or a logical negation of a boolean variable (operand {index} is '{op}')")

  def replace(self, ops, attrs):
    return None

  def determine_valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bool()

  def determine_value(self, expr, op_values):
    return any(op_values)

  def map_to_target(self, expr, op_target_mapping, target_ctx):

    # TODO: Check target is cnf.

    lit = target_ctx.valtype.bool.variable(name=
        ExprUtils.make_variable_name_from_expr(expr))

    # For each op: lit => oplit
    for oplit in op_target_mapping:
      target_ctx.add_constraint(target_ctx.cnf.logical_or(
        oplit,
        self._make_not(target_ctx, lit)))

    # not oplit_0 and ... and not oplit_n => not lit
    target_ctx.add_constraint(target_ctx.cnf.logical_or(
        *[oplit for oplit in op_target_mapping],
        self._make_not(target_ctx, lit)))

    return lit