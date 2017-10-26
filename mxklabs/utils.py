import re

# Compile this regex once.
_camel_case_regex = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

''' Helper functions. '''
class Utils(object):

  @staticmethod
  def camel_case_to_underscore(string):
    return _camel_case_regex.sub(r'_\1', string).lower()
  
  @staticmethod
  def underscore_to_camel_case(string):
    return "".join([noun.capitalize() for noun in string.split('_')])
  
  @staticmethod
  def camel_case_to_dashed(string):
    return _camel_case_regex.sub(r'-\1', string).lower()
  
  @staticmethod
  def dashed_to_camel_case(string):
    return "".join([noun.capitalize() for noun in string.split('-')])

# NOTE: I'd have rather used functools.lru_cache to achieve memoisation but it's not available 
# in Python 2.x. Hence, I'm using a solution from stack overflow: 
# https://stackoverflow.com/questions/815110/is-there-a-decorator-to-simply-cache-function-return-values

''' Memoise decorator. '''
def Memoise(function):
  memo = {}
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper
