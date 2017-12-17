import atexit
import inspect
from itertools import tee
import json
import re

# Compile these regexes once.
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

  @staticmethod
  def is_iterable(obj):
      try:
          it = iter(obj)
          return True
      except:
          return False

  ''' Return classes in module that inherit from base_class, but not base_class itself. '''
  @staticmethod
  def get_derived_classes(module, base_class):
      result = []
      for name, obj in inspect.getmembers(module):
          if inspect.isclass(obj) and issubclass(obj, base_class) and obj != base_class:
              result.append(obj)
      return result

  ''' Returns true if class object has a function of the specified name. Can be used for testing interfaces. '''
  @staticmethod
  def class_has_function(class_, function_name):
      if hasattr(class_, function_name):
          return inspect.isfunction(getattr(class_, function_name)) \
              or inspect.ismethod(getattr(class_, function_name))
      else:
          return False

  @staticmethod
  def check_precondition(precondition):
      if not precondition:
          raise RuntimeError('precondition violated')
    
  @staticmethod
  def product(*iterables, **kwargs):
      """
      Create an iterable cartesian product of iterables. Unlike itertools's
      product this product iterates over all iterables on-the-fly.
      :param iterables: The components of the product.
      :param kwargs: Undocumented.
      :return:
      """
      if len(iterables) == 0:
          yield ()
      else:
          iterables = iterables * kwargs.get('repeat', 1)
          it = iterables[0]

          for item in it() if callable(it) else iter(it):
              iterables_tee = list(map(tee, iterables[1:]))
              iterables[1:] = [it1 for it1, it2 in iterables_tee]
              iterable_copy = [it2 for it1, it2 in iterables_tee]

              for items in Utils.product(*iterable_copy):
                  yield (item,) + items


''' Memoise decorator. '''

def memoise(function):
    """
    You can use this function as a decorator (a callable object that given
    a function as a parameter returns another function) on other functions to
    memoise calls to said function (i.e. avoid repeat calculations for the same
    parameters by storing them in memory).

    NOTE: I'd have rather used functools.lru_cache to achieve memoisation but
    it's not available in Python 2.x. Instead we're using a custom implementation.
    """
    cache = {}
    def memoise_wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            result = function(*args)
            cache[args] = result
            return result
    return memoise_wrapper


def memoise_to_file(filename):
    """
    You can call this function with a filename parameter to generate a decorator
    (a callable object that given a function as a parameter returns another
    function) which can be placed on other functions to persistently memoise
    calls to said function (i.e. avoid repeat calculations for the same
    parameters by storing them in on disk).

    The returned decorators implement persistent memoisation implemented by
    dumping results to a JSON file. For this to work both parameters and return
    values of function MUST be serialisable to JSON.
    :param filename: The filename to cache stuff to.
    :return: A memoising decorator function.
    """
    def decorator(function):

        def load_cache_from_disk():
            try:
                cache = {}
                cache_as_json = json.load(open(filename, 'r'))
                for entry in cache_as_json:
                    cache[tuple(entry['args'])] = entry['result']
                return cache

            except (IOError, ValueError):
                return {}

        def save_cache_to_disk(cache):
            try:
                cache_as_json = []
                for params, value in cache.items():
                    cache_as_json.append({'args': params, 'result': value})
                json.dump(cache_as_json, open(filename, 'w'))
            except (IOError, ValueError):
                print("Unable to memoise '{}'".format(filename))

        # Load from disk when decorator is generated.
        cache = load_cache_from_disk()
        # Save to disk on program exit.
        atexit.register(lambda: save_cache_to_disk(cache))

        def memoise_wrapper(*args):

            if args not in cache:
                result = function(*args)
                cache[args] = result
                return result

            return cache[args]

        return memoise_wrapper

    return decorator