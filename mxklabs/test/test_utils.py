import unittest

import mxklabs as mxk

class Test_Utils(unittest.TestCase):
  
  def test_Utils_is_camel_case(self):
    self.assertTrue(mxk.Utils.is_camel_case("IsCamelCase"))
    self.assertFalse(mxk.Utils.is_camel_case("isNotCamelCase"))
    self.assertFalse(mxk.Utils.is_camel_case("is_not_camel_case"))

  def test_Utils_is_snake_case(self):
    self.assertTrue(mxk.Utils.is_snake_case("is_snake_case"))
    self.assertFalse(mxk.Utils.is_snake_case("IsNotSnakeCase"))
    self.assertFalse(mxk.Utils.is_snake_case("is-not-snake-case"))

  def test_Utils_is_kebab_case(self):
    self.assertTrue(mxk.Utils.is_kebab_case("is-kebab-case"))
    self.assertFalse(mxk.Utils.is_kebab_case("IsNotKebabCase"))
    self.assertFalse(mxk.Utils.is_kebab_case("is_not_kebab_case"))
  
  def test_Utils_camel_case_to_snake_case(self):
    self.assertEqual("test_word", mxk.Utils.camel_case_to_snake_case("TestWord"))
  
  def test_Utils_camel_case_to_kebab_case(self):
    self.assertEqual("test-word", mxk.Utils.camel_case_to_kebab_case("TestWord"))
  
  def test_Utils_snake_case_to_camel_case(self):
    self.assertEqual("TestWord", mxk.Utils.snake_case_to_camel_case("test_word"))
    
  def test_Utils_snake_case_to_kebab_case(self):
    self.assertEqual("test-word", mxk.Utils.snake_case_to_kebab_case("test_word"))
    
  def test_Utils_kebab_case_to_camel_case(self):
    self.assertEqual("TestWord", mxk.Utils.kebab_case_to_camel_case("test-word"))
    
  def test_Utils_kebab_case_to_snake_case(self):
    self.assertEqual("test_word", mxk.Utils.kebab_case_to_snake_case("test-word"))