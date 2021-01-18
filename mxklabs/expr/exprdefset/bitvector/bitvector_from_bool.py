from .exprdef import BitvectorExprDef
from ...exprutils import ExprUtils

class BitvectorFromBool(BitvectorExprDef):

  def __init__(self, **kwargs):
    BitvectorExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting as many bool ops as width bits, all boolean.
    ExprUtils.basic_attrs_check(self.id(), {'width':int}, attrs)
    ExprUtils.basic_ops_check(self.id(), attrs['width'], attrs['width'], self._ctx.valtype.bool(), ops)

    if (attrs['width'] != len(ops)):
      raise RuntimeError(f"'{self.id}' expected {attrs['width']} operands (got {len(ops)})")
    if (attrs['index'] < 0 or attrs['index'] >= attrs['width']):
      raise RuntimeError(f"'{self.id}' invalid value for 'index' (got {attrs['index']}, expected value in [{0, attrs['width']}-1])")

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bitvector(width=attrs['width'])

  def evaluate(self, expr, op_values):
    return expr.valtype.valtype_def().convert_booltup_to_value(expr.valtype(), op_values)

  def has_feature(self, featurestr):
    if featurestr == 'simplify':
      return True
    if featurestr == 'canonicalize':
      return True
    return False

  def simplify(self, expr):
    # bitvector_from_bools(e0, ..., e_i=const, e7) => e_i
    if any([self._ctx.is_constant(op) and not op.value() for op in expr.ops()]):
      return self._ctx.constant(value=False, valtype=self._ctx.valtype.bool())

    # logical_and(1, ..., 1) => 1
    if all([self._ctx.is_constant(op) and op.value() for op in expr.ops()]):
      return self._ctx.constant(value=True, valtype=self._ctx.valtype.bool())

    # logical_and(e, ..., logical_not(e)) => 0
    negops = [self._ctx.expr.logical_not(op) for op in expr.ops()]
    if any([op in negops for op in expr.ops()]):
      return self._ctx.constant(value=False, valtype=self._ctx.valtype.bool())

    # logical_and(e) => e
    if len(expr.ops()) == 1:
      return expr.ops()[0]

    # Remove any true ops.
    filtered_ops = [op for op in expr.ops() if not self._ctx.is_constant(op) or not op.value()]
    if len(filtered_ops) < len(expr.ops()):
      # Can't be zero because we would have simplified above.
      assert(len(filtered_ops) > 0)
      # One non-true op, simplify to that op.
      if len(filtered_ops) == 1:
        return filtered_ops[0]
      # Multiple, just remove the terms.
      else:
        return self._ctx.expr.logical_and(filtered_ops)

    # Can't simplify.
    return expr

  def canonicalize(self, expr):
    # Sort by operand hash.
    ops = list(expr.ops())
    new_ops = sorted(ops, key=hash)
    if new_ops != ops:
      return self._ctx.expr.logical_and(*new_ops, simplify=True)

    return expr
