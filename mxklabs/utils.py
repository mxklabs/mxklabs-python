import inspect
import re

# Compile this regex once.
_convert_camel_case_regex = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
_check_camel_case_regex = re.compile('^([A-Z][a-z]*)+$')
_check_snake_case_regex = re.compile('^[a-z]+(\_[a-z]+)*$')
_check_kebab_case_regex = re.compile('^[a-z]+(\-[a-z]+)*$')

''' Helper functions. '''
class Utils(object):

  @staticmethod
  def is_camel_case(string):
    return bool(_check_camel_case_regex.match(string))
  
  @staticmethod
  def is_snake_case(string):
    return bool(_check_snake_case_regex.match(string))

  @staticmethod
  def is_kebab_case(string):
    return bool(_check_kebab_case_regex.match(string))
    
  @staticmethod
  def camel_case_to_snake_case(string):
    return _convert_camel_case_regex.sub(r'_\1', string).lower()
  
  @staticmethod
  def camel_case_to_kebab_case(string):
    return _convert_camel_case_regex.sub(r'-\1', string).lower()
  
  @staticmethod
  def snake_case_to_camel_case(string):
    return "".join([noun.capitalize() for noun in string.split('_')])
  
  @staticmethod
  def snake_case_to_kebab_case(string):
    return "-".join([noun for noun in string.split('_')])
  
  @staticmethod
  def kebab_case_to_camel_case(string):
    return "".join([noun.capitalize() for noun in string.split('-')])
  
  @staticmethod
  def kebab_case_to_snake_case(string):
    return "_".join([noun for noun in string.split('-')])
  
  ''' Return classes in module that inherit from base_class, but not base_class itself. '''
  @staticmethod
  def get_derived_classes(module, base_class):
    result = []
    for name, obj in inspect.getmembers(module):
      if inspect.isclass(obj) and issubclass(obj, base_class) and obj != base_class:
          result.append(obj)
    return result
    
    
  
# NOTE: I'd have rather used functools.lru_cache to achieve memoisation but it's not available 
# in Python 2.x. Hence, I'm using a solution from stack overflow: 
# https://stackoverflow.com/questions/815110/is-there-a-decorator-to-simply-cache-function-return-values

''' Memoise decorator. '''
def memoise(function):
  memo = {}
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper