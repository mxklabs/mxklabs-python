import re

class ValtypeDef:

  id_regex = re.compile(r'(?<!^)(?=[A-Z])')

  def __init__(self, ctx, package):
    self._ctx = ctx
    self._baseid = ValtypeDef.id_regex.sub('_', self.__class__.__name__).lower()
    self._id = f"{package}.{self._baseid}"

  def id(self):
    """
    Return the fully qualified id, e.g. 'mxklabs.expr.valtypedef.bool'.
    """
    return self._id

  def baseid(self):
    """
    Return the last part of the id, e.g. 'bool', defaults to snake case of
    the class' name.
    """
    return self._baseid

  def validate(self, sub_valtypes, attrs):
    """
    This method is called prior to the construction of a valtype.

    Determine whether a list of sub valtypes and a dictionary of attributes are valid
    for this type of valtype. Raise an exception if this is not the case.
    """

  def validate_value(self, valtype, )    

  def is_valid_value(self, valtype, value):
    if type(value) == int:
      return value == 0 or value == 1
    if type(value) == bool:
      return True

  def values(self, valtype):
    yield False
    yield True

  def num_values(self, valtype):
    return 2

  def value_to_str(self, valtype, value):
    return 'False' if not value else 'True'