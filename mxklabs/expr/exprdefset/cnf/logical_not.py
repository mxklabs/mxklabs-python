from .exprdef import CnfExprDef
from ...exprutils import ExprUtils

class LogicalNot(CnfExprDef):

  def __init__(self, **kwargs):
    CnfExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting one or more operands, all boolean, no attributes.
    ExprUtils.basic_ops_check(self.id(), 1, 1, self._ctx.valtype.bool(), ops)
    ExprUtils.basic_attrs_check(self.id(), {}, attrs)
    # Check operand is a boolean variable.
    if not (self._ctx.is_variable(ops[0]) and self._ctx.valtype.is_bool(ops[0].valtype())):
      raise RuntimeError(f"'{self.id()}' operand must be a boolean variable (operand is '{ops[0]}')")

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bool()

  def evaluate(self, expr, op_values):
    return not op_values[0]

def has_feature(self, featurestr):
    return False