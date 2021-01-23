from ...valtypedef import ValtypeDef
from ...exprutils import ExprUtils

class BoolValtypeDef(ValtypeDef):

  def __init__(self, ctx):
    ValtypeDef.__init__(self, ctx, baseid='bool', package='mxklabs.expr.valtype')

  def validate(self, sub_valtypes, attrs):
    # Check sub_valtypes.
    ExprUtils.basic_sub_valtypes_check(self.id(), 0, 0, None, sub_valtypes)
    # No attributes.
    ExprUtils.basic_attrs_check(self.id(), {}, attrs)

  def validate_value(self, valtype, value):
    return value in [True, False]

  def num_values(self, valtype):
    return 2

  def values(self, valtype):
    yield False
    yield True

  def convert_userobj_to_value(self, valtype, userobj):
    if type(userobj) == int:
      if userobj == 0:
        return False
      elif userobj == 1:
        return True
    if type(userobj) == bool:
      return userobj
    raise RuntimeError(f"'{userobj}' is not a valid value for valtype '{valtype}' (expected boolean)")

  def convert_value_to_str(self, valtype, value):
    return "1" if value else "0"

  def booltup_size(self, valtype):
    return 1

  def convert_value_to_booltup(self, valtype, value):
    return [value]

  def convert_booltup_to_value(self, valtype, value):
    return value[0]

  def get_bool_expr(self, expr, index):
    assert(index == 0)
    return expr