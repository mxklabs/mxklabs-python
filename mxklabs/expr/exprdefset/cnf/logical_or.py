from .exprdef import CnfExprDef
from ...exprutils import ExprUtils

class LogicalOr(CnfExprDef):

  def __init__(self, **kwargs):
    CnfExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting one or more operands, all boolean, no attributes.
    ExprUtils.basic_ops_check(self.id(), 1, None, self._ctx.valtype.bool(), ops)
    ExprUtils.basic_attrs_check(self.id(), {}, attrs)
    # Require all operands to either be boolean variables or negations of boolean variables.
    for index, op in zip(range(len(ops)), ops):
      if (not (self._ctx.is_variable(op) and self._ctx.valtype.is_bool(op.valtype()))) and \
         (not self._ctx.expr.is_logical_not(op)):
        raise RuntimeError(f"'{self.id()}' operands must be either a boolean variable or a logical negation of a boolean variable (operand {index} is '{op}')")

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bool()

  def evaluate(self, expr, op_values):
    return any(op_values)

  def has_feature(self, featurestr):
    return False
