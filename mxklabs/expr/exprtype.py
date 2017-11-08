import functools
import itertools
import operator
import six

import mxklabs.utils

''' Simple type. '''

class ExprType(object):
  
  def __init__(self, typestr, values, num_values):
    
    self._typestr = typestr
    self._values = values
    self._num_values = num_values
    
  def __eq__(self, other):
    if not isinstance(other, ExprType):
      return False
    return self._typestr == other._typestr
  
  def __hash__(self):
    return hash(self._typestr)
  
  def __str__(self):
    return self._typestr  
  
  def __repr__(self):
    return self._typestr
  
  ''' An iterable list of values. For large types with the number of values exceeding, say, 2^10, these values
      must be constructed on-the-fly using e.g. six.moves.range. '''
  def values(self):
    return self._values
  
  ''' The number of values. '''
  def num_values(self):
    return self._num_values
  
  ''' Returns true if the value is in values(). For large types with the number of values exceeding, say, 2^10, 
      this function must not rely on iterating over all values'''
  def is_valid_value(self, value):
    if self.num_values() <= (2 ** 10):
      return value in self._values
    else:
      raise Exception("Not implemented for class {classname} (with {number_of_values} "
                      "values)".format(classname=self.__class__.__name__, values=self.num_values()))
  
  ''' Number of booleans to encode value. '''
  def littup_size(self):
    return 1
  
  ''' '''
  def littup_to_value(self, littup):
    
    pass
  
  def value_to_littup(self, value):
    return (value,)

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
    super().__init__("bool", values=[(False,),(True,)], num_values=2)
    
  def user_friendly_value_to_littup_value(self, user_friendly_value):
    return (user_friendly_value,)
  
  def littup_value_to_user_friendly_value(self, littup_value):
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

