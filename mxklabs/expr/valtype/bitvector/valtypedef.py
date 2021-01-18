from ...valtypedef import ValtypeDef
from ...exprutils import ExprUtils

class BitvectorValtypeDef(ValtypeDef):

  def __init__(self, ctx):
    ValtypeDef.__init__(self, ctx, baseid='bitvector', package='mxklabs.expr.valtype')

  def validate(self, sub_valtypes, attrs):
    # One attribute: width.
    ExprUtils.basic_attrs_check(self.id(), {'width':int}, attrs)
    # Check sub_valtypes.
    ExprUtils.basic_sub_valtypes_check(self.id(), 0, 0, None, sub_valtypes)

  def validate_value(self, valtype, value):
    return value in [True, False]

  def num_values(self, valtype):
    return 2**valtype.width

  def values(self, valtype):
    return range(0, 2**valtype.width)

  def convert_userobj_to_value(self, valtype, userobj):
    if type(userobj) == int:
      if userobj >= 0 and userobj < 2**valtype.width:
        return userobj
    raise RuntimeError(f"'{userobj}' is not a valid value for valtype '{valtype}' (expected boolean)")

  def convert_value_to_str(self, valtype, value):
    booltup_value = self.convert_value_to_booltup(valtype, value)
    bitstr = "".join(["1" if bit else "0" for bit in reversed(booltup_value)])
    return f"{bin(bitstr)} ({value:d})"

  def booltup_size(self, valtype):
    return valtype.width

  def convert_value_to_booltup(self, valtype, value):
    return [((value >> bit) & 1) == 1 for bit in range(valtype.width)]

  def convert_booltup_to_value(self, valtype, value):
    return sum(1 << bit if value[0] else 0 for bit in range(valtype.width))