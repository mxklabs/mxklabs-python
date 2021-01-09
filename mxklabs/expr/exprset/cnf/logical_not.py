from .cnfexprdef import CnfExprDef
from ...exprutils import ExprUtils

class LogicalNot(CnfExprDef):

  def __init__(self, ctx):
    CnfExprDef.__init__(self, ctx)

  def validate(self, ops, attrs):
    # Expecting one or more operands, all boolean, no attributes.
    ExprUtils.basicOpsAndAttrsCheck(self.id(), 1, 1, self._ctx.bool(), ops, [], attrs)
    # Check operand is a boolean variable.
    if not self._ctx.is_variable(ops[0]) or ops[0].valtype != self._ctx.bool():
      raise RuntimeError(f"'{self.id()}' must negate a variable (got operand '{ops[0]}')")

  def replace(self, ops, attrs):
    return None

  def determine_valtype(self, ops, attrs, op_valtypes):
    return self._ctx.bool()

  def determine_value(self, expr, op_values):
    return not op_values[0]

  def map_to_target(self, expr, op_target_mapping, target_ctx):

    # TODO: Check target is cnf.
    return make_not(target_ctx, op_target_mapping[0])
