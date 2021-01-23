import re

class ValtypeDef:

  def __init__(self, ctx, baseid, package):
    self._ctx = ctx
    self._baseid = baseid
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
    raise RuntimeError(f"'{self.__class__.__name__}.validate' has not been implemented")

  def validate_value(self, valtype, value):
    """
    Determine if a python object is an object representing a valid value of valtype.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.validate_value' has not been implemented")

  def num_values(self, valtype):
    """
    Determine the number of values of a valtype.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.num_values' has not been implemented")

  def values(self, valtype):
    """
    A generator of values of a valtype.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.values' has not been implemented")

  def convert_userobj_to_value(self, valtype, userobj):
    """
    Convert a user's input value to a valid value. If the userobj cannot be converted,
    raise an exception.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.convert_userobj_to_value' has not been implemented")

  def convert_value_to_str(self, valtype, value):
    """
    Convert a valtype value to a string that is user-friendly.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.convert_value_to_str' has not been implemented")

  def booltup_size(self, valtype):
    """
    Return the number of booleans required to represent this value when converting to CNF.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.booltup_size' has not been implemented")

  def convert_value_to_booltup(self, valtype, value):
    """
    Convert value to booltup value.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.convert_value_to_booltup' has not been implemented")

  def convert_booltup_to_value(self, valtype, value):
    """
    Convert booltup value to real value.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.convert_booltup_to_value' has not been implemented")

  def get_bool_expr(self, expr, index):
    """
    Get expression that extracts the index-th boolean from an expr with this valtype.
    """
    raise RuntimeError(f"'{self.__class__.__name__}.get_bool_expr' has not been implemented")

