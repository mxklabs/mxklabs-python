from .exprdef import LogicalExprDef
from ...exprutils import ExprUtils

class LogicalXor(LogicalExprDef):

  def __init__(self, **kwargs):
    LogicalExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting two operands, all boolean, no attributes.
    ExprUtils.basic_ops_check(self.id(), 2, 2, self._ctx.valtype.bool(), ops)
    ExprUtils.basic_attrs_check(self.id(), {}, attrs)

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bool()

  def evaluate(self, expr, op_values):
    return op_values[0] != op_values[1]

  def has_feature(self, featurestr):
    if featurestr == 'simplify':
      return True
    elif featurestr == 'cnf':
      return True
    return False

  def simplify(self, expr):
    op0 = expr.ops()[0]
    op1 = expr.ops()[1]

    # logical_xor(const0, const1) => const0 ^ const1
    if self._ctx.is_constant(op0) and self._ctx.is_constant(op1):
      return self._ctx.constant(value=op0.value()!=op1.value(), valtype=self._ctx.valtype.bool())

    # logical_xor(e, e) => false
    if op0 == op1:
      return self._ctx.constant(value=False, valtype=self._ctx.valtype.bool())

    # logical_xor(logical_not(e), e) => true
    if self._ctx.expr.is_logical_not(op0) and op0.ops()[0] == op1:
      return self._ctx.constant(value=True, valtype=self._ctx.valtype.bool())

    # logical_xor(e, logical_not(e)) => true
    if self._ctx.expr.is_logical_not(op1) and op1.ops()[0] == op0:
      return self._ctx.constant(value=True, valtype=self._ctx.valtype.bool())

    # if one op is constant
    if self._ctx.is_constant(op0) or self._ctx.is_constant(op1):
      const_op = op0 if self._ctx.is_constant(op0) else op1
      other_op = op1 if self._ctx.is_constant(op0) else op0

      if const_op.value():
        if self._ctx.expr.is_logical_not(other_op):
          return other_op.ops()[0]
        else:
          return self._ctx.expr.logical_not(other_op)
      else:
        return other_op

    return expr

  def canonicalize(self, expr):
    op0 = expr.ops()[0]
    op1 = expr.ops()[1]

    # Sort by operand hash.
    if hash(op1) < hash(op0):
      return self._ctx.expr.logical_xor(op1, op0)

    return expr
