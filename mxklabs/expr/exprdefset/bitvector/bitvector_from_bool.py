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

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bitvector(width=attrs['width'])

  def evaluate(self, expr, op_values):
    return expr.valtype().valtype_def().convert_booltup_to_value(expr.valtype(), op_values)

  def has_feature(self, featurestr):
    if featurestr == 'simplify':
      return True
    return False

  def simplify(self, expr):
    # bitvector_from_bool(const0, ..., const_i) => const
    if all([self._ctx.is_constant(op) for op in expr.ops()]):
      booltup_value = [expr.ops()[bit].value() for bit in range(expr.attrs()['width'])]
      value = expr.valtype().valtype_def().convert_booltup_to_value(expr.valtype(), booltup_value)
      return self._ctx.constant(value=value, valtype=expr.valtype())

    # Can't simplify.
    return expr

