import unittest

import mxklabs.utils

class Tests(unittest.TestCase):
  
  def test_camel_case_to_underscore(self):
    self.assertEquals("this_is_camel_case", mxklabs.utils.Utils.camel_case_to_underscore("ThisIsCamelCase"))
  
  def test_dashed_to_camel_case(self):
    self.assertEquals("ThisIsCamelCase", mxklabs.utils.Utils.underscore_to_camel_case("this_is_camel_case"))
    
  def test_camel_case_to_dashed(self):
    self.assertEquals("this-is-camel-case", mxklabs.utils.Utils.camel_case_to_dashed("ThisIsCamelCase"))
    
  def test_dashed_to_camel_case(self):
    self.assertEquals("ThisIsCamelCase", mxklabs.utils.Utils.dashed_to_camel_case("this-is-camel-case"))