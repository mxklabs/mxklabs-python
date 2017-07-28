import re

''' Helper functions. '''

camel_case_regex = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

class Utils(object):

  @staticmethod
  def camel_case_to_underscore(string):
    return camel_case_regex.sub(r'_\1', string).lower()
  
  @staticmethod
  def underscore_to_camel_case(string):
    return "".join([noun.capitalize() for noun in string.split('_')])
  
import unittest

class Tests(unittest.TestCase):
  
  def test_camel_case_to_underscore(self):
    self.assertEquals("this_is_camel_case", Utils.camel_case_to_underscore("ThisIsCamelCase"))
    
  def test_underscore_to_camel_case(self):
    self.assertEquals("ThisIsCamelCase", Utils.underscore_to_camel_case("this_is_camel_case"))