from mxklabs.expr import exprtype as et

''' 
    A container that holds the value of an expression. The value is represented with
    both a user-facing logical value and the internal representation: a tuple of bools.
    We rely on ExprType objects to convert from one to the other representation. The
    logical representation can be given as the second unnamed argument whereas
    the the tuple representation has to be named. The constructor for ExprValue expects 
    exactly one representation.
    
    Examples:
    
    v1 = mxklabs.ExprValue(et.Bool(), False)
    v1 = mxklabs.ExprValue(et.Bool(), littup_value=(False,))
''' 
class ExprValue(object):

  def __init__(self, type, logical_value=None, littup_value=None):

    assert(isinstance(type, et.ExprType))
    assert((logical_value == None) != (littup_value == None))
    
    if logical_value != None:
      self._type = type
      self._logical_value = logical_value
      self._littup_value = self._type.logical_value_to_littup_value(self._logical_value)
    else:
      self._type = type
      self._littup_value = littup_value
      self._logical_value = self._type.littup_value_to_logical_value(self._littup_value)

  def __eq__(self, other):
    return self._littup_value == other._littup_value
  
  def __hash__(self):
    return hash(self._littup_value)
  
  def __str__(self):
    return __repr__(self._logical_value)
  
  def __repr__(self):
    return __repr__(self._logical_value)

  def logical_value():
    return self._logical_value

  def littup_value():
    return self._littup_value
    