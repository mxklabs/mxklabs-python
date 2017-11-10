import functools
import itertools
import operator
import six

import mxklabs.utils

''' 
    A container that holds the value of an expression. The value is represented with
    both a user-facing logical value and a tuple of bools.
    We rely on ExprType objects to convert from one representation to the other. The
    logical representation can be given as the second unnamed argument whereas
    the the tuple representation has to be named. The constructor for ExprValue expects 
    exactly one representation.
    
    Examples:
    
    v1 = mxklabs.ExprValue(Bool(), False)
    v1 = mxklabs.ExprValue(Bool(), littup_value=(False,))
''' 
class ExprValue(object):

  def __init__(self, type, user_value=None, littup_value=None):

    assert(isinstance(type, ExprType))
    assert((user_value == None) != (littup_value == None))
    
    if user_value != None:
      assert(type.is_valid_user_value(user_value=user_value))
      self._type = type
      self._user_value = user_value
      self._littup_value = self._type.user_value_to_littup_value(self._user_value)

    if littup_value != None:
      assert(type.is_valid_littup_value(littup_value=littup_value))
      self._type = type
      self._littup_value = littup_value
      self._user_value = self._type.littup_value_to_user_value(self._littup_value)

  def __eq__(self, other):
    assert(isinstance(other, ExprValue))
    return self._littup_value == other._littup_value
  
  def __hash__(self):
    return hash(self._littup_value)
  
  def __str__(self):
    return str(self._user_value)
  
  def __repr__(self):
    return repr(self._user_value)

  def user_value(self):
    return self._user_value

  def littup_value(self):
    return self._littup_value
    
''' A class representing a type of an Expr object. Instances of this class are expected to '''

class ExprType(object):
  
  def __init__(self, typestr):    
    self._typestr = typestr

  def __eq__(self, other):
    assert (isinstance(other, ExprType))
    return self._typestr == other._typestr

  def __ne__(self, other):
    assert (isinstance(other, ExprType))
    return self._typestr != other._typestr

  def __hash__(self):
    return hash(self._typestr)
  
  def __str__(self):
    return self._typestr  
  
  def __repr__(self):
    return self._typestr

  ''' Helper function to decide if something is a subclass of ExprType. '''
  @staticmethod
  def is_exprtype(type):
    try:
      return isinstance(type, ExprType)
    except Exception as e:
      return False

''' Unparameterised types. '''

class Bool(ExprType):

  def __init__(self):
    self._values = [ExprValue(type=self, user_value=False), ExprValue(type=self, user_value=True)]
    self._num_values = len(self._values)

    ExprType.__init__(self, "bool")

  ''' An iterable list of values. For large types with the number of values exceeding, say, 2^10, these values
      must be constructed on-the-fly using e.g. six.moves.range. '''
  def values(self):
    return self._values
  
  ''' The number of values. '''
  def num_values(self):
    return self._num_values
  
  ''' Number of elements in a boolean tuple. '''
  def littup_size(self):
    return 1
  
  ''' Any bool is a valid user_value. '''
  def is_valid_user_value(self, user_value):
    return type(user_value) == bool
  
  ''' Any tuple with a single element that is a bool is a valid littup_value. '''
  def is_valid_littup_value(self, littup_value):
    return type(littup_value) == tuple and len(littup_value) == 1 and type(littup_value[0]) == bool
  
  ''' Convert user_value to littup_value. '''
  def user_value_to_littup_value(self, user_value):
    assert(self.is_valid_user_value(user_value))
    return (user_value,)
  
  ''' Convert littup_value to user_value. '''
  def littup_value_to_user_value(self, littup_value):
    assert(self.is_valid_littup_value(littup_value))
    return littup_value[0]
  

''' Class for product of types. '''

#class Product(ExprType):
#  
#  def __init__(self, subtypes, typestr=None):
#
#    if len(subtypes) < 1:
#      raise Exception("a product type must have at least one subtype")
#    for subtype in subtypes:
#      if not isinstance(subtype, ExprType):
#        raise Exception("the 'subtype' parameter of type 'Product' must be an interable over 'ExprType' (found '{type}' subtype)".format(
#                        type=subtype))
#
#    super().__init__(
#        # Use the given typestr if there is one. If not, use something like "(Bool,Bool)".
#        typestr="(" + ",".join([t._typestr for t in subtypes]) + ")" if typestr==None else typestr,
#        # Produce a values iterator (don't be explicit due to combinatorial explosions).
#        values=itertools.product(*([t.values() for t in subtypes])),
#        # Compute number of values.
#        num_values=functools.reduce(operator.mul, [s.num_values() for s in subtypes]))
#    
#    self._subtypes = subtypes
#    
#    
#    def is_valid_value(self, value):
#      if len(value) != len(self._subtypes):
#        return False
#      else:
#        return all([self._subtypes[s].is_valid_value(value[s]) for s in range(len(self._subtypes))])
#
#''' Parameterised types. '''
#
#class BitVector(Product):
#    
#  def __init__(self, bits):
#    super().__init__(subtypes=([Bool()] * bits), typestr=("uint%d" % bits))
#
#  @staticmethod
#  def int_to_value(bits, n):
#    return tuple([(((1 << b) & n) != 0,) for b in range(bits)])
#
#  @staticmethod
#  def value_to_int(bits, value):
#    return sum([(1 << b) if value[b][0] else 0 for b in range(len(value))])

