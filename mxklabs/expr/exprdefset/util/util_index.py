from .exprdef import UtilExprDef
from ...exprutils import ExprUtils

class UtilIndex(UtilExprDef):

  def __init__(self, **kwargs):
    UtilExprDef.__init__(self, **kwargs)

  def validate(self, ops, attrs):
    # Expecting one or more operands, all boolean, no attributes.
    ExprUtils.basic_attrs_check(self.id(), {'index':int}, attrs)
    valtype_checker = lambda valtype, index: self._ctx.valtype.is_bitvector(valtype)
    ExprUtils.basic_ops_check(self.id(), 1, 1, valtype_checker, ops)

    if (attrs['index'] < 0 or attrs['index'] >= ops[0].valtype().attrs()['width']):
      raise RuntimeError(f"'{self.id}' invalid value for 'index' (got {attrs['index']}, expected value in [{0, attrs['width']}-1])")

  def valtype(self, ops, attrs, op_valtypes):
    return self._ctx.valtype.bool()

  def evaluate(self, expr, op_values):
    return (op_values[0] >> expr.attrs()['index']) & 1

  def has_feature(self, featurestr):
    if featurestr == 'simplify':
      return True
    return False

  def simplify(self, expr):
    index = expr.attrs()['index']

    # index(const, index=n) => (const >> n) & 1
    if self._ctx.is_constant(expr.ops()[0]):
      op_value = expr.ops()[0].value()
      op_valtype = expr.ops()[0].valtype()
      op_valtype_def = op_valtype.valtype_def()
      op_booltup_value = op_valtype_def.convert_value_to_booltup(op_valtype, op_value)
      return self._ctx.constant(value=op_booltup_value[index], valtype=self._ctx.valtype.bool())

    # TODO: What if it's a to_bool over from_bool?

    # Can't simplify.
    return expr


