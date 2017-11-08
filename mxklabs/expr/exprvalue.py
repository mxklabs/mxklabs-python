from mxklabs.expr import exprtype as et

''' 
    A container that holds the value of an expression. The value is represented with
    both a user-facing friendly value and the internal representation: a tuple of bools.
    We rely on ExprType objects to convert from one to the other representation. The
    user-friendly representation can be given as the second unnamed argument whereas
    the the tuple representation has to be named. The constructor for ExprValue expects 
    exactly one representation.
    
    Examples:
    
    v1 = mxklabs.ExprValue(et.Bool(), False)
    v1 = mxklabs.ExprValue(et.Bool(), littup_value=(False,))
''' 
class ExprValue(object):

  def __init__(self, type, user_friendly_value=None, littup_value=None):

    assert(isinstance(type, et.ExprType))
    assert((user_friendly_value == None) != (littup_value == None))
    
    if user_friendly_value != None:
      self._type = type
      self._user_friendly_value = user_friendly_value
      self._littup_value = self._type.user_friendly_value_to_littup_value(self._user_friendly_value)
    else:
      self._type = type
      self._littup_value = littup_value
      self._user_friendly_value = self._type.littup_value_to_user_friendly_value(self._littup_value)
      
  def value():
    return self._user_friendly_value

  def littup_value():
    return self._littup_value
    