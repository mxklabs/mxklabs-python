import functools
import itertools
import six

# I'd like to use functools.lru_cache to achieve memoisation but it's not available 
# on Python 2.x. Hence, I'm using one I found on stack overflow: 
# https://stackoverflow.com/questions/815110/is-there-a-decorator-to-simply-cache-function-return-values

def memoize(function):
  memo = {}
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper

''' Simple type. '''
class Type(object):
  
  def __init__(self, typestr, values, num_values):
    self._typestr = typestr
    self._values = values
    self._num_values = num_values
    
  def __eq__(self, other):
    return self._typestr == other._typestr
  
  def __hash__(self):
    return hash(self._typestr)
  
  def __str__(self):
    return self._typestr  
  
  def __repr__(self):
    return self._typestr
  
  def values(self):
    return self._values
  
  def num_values(self):
    return self._num_values
  
''' Product of types. '''
class Product(Type):
  
  def __init__(self, subtypes):
    self.subtypes = subtypes
    Type.__init__(self, 
      typestr="(" + ",".join([t._typestr for t in subtypes]) + ")",
      values=itertools.product(subtypes),
      num_values=functools.reduce(lambda x, y : x * y, subtypes.num_values()))

''' Unparameterised types. '''

Bool = Type("bool", values=[False,True], num_values=2)

''' Parameterised types. '''

@memoize 
def BitVector(bits): return Type("uint%d" % bits, values=six.moves.range(2**bits), num_values=2**bits)


import unittest

class Tests(unittest.TestCase):
  
  def test_Bool(self):    
    self.assertEqual("bool", str(Bool))
    self.assertEqual([False, True], [value for value in Bool.values()])
    self.assertEqual(2, Bool.num_values())
    
  def test_BitVector(self):    
    self.assertEqual("uint3", str(BitVector(3)))
    self.assertEqual([0,1,2,3,4,5,6,7], [value for value in BitVector(3).values()])
    self.assertEqual(8, BitVector(3).num_values())