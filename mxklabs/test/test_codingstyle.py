import inspect as i
import re
import unittest

import mxklabs as mxk

class Test_CodingStyle(unittest.TestCase):

  CAMEL_CASE_REGEX = '(([A-Z][a-z]*[0-9]*)+)'
  SNAKE_CASE_REGEX = '([a-z]+(\_[a-z]+[0-9]*)*)'
  
  ''' Helper function. '''
  def _check_names(self, names, regex):
    for name in names:
      assertMsg = "'{name}' violates naming conventions'".format(name=name, type=type)
      self.assertTrue(bool(regex.match(name)), assertMsg)
  
  ''' Check all classes in mxk are in CamelCase. '''
  def test_CodingStyle_class_name(self):
    
    # Make a regex for what are acceptable class names.
    acceptable_classnames_regex = re.compile('^' + Test_CodingStyle.CAMEL_CASE_REGEX + '$')
    
    # Get all class names.
    classnames = [name for name, member in i.getmembers(mxk) if i.isclass(member)]

    # Check 'em.
    self._check_names(classnames, acceptable_classnames_regex)
            
  ''' Check all method names in mxk are in 'snake_case' or '__snake_case__'. '''
  def test_CodingStyle_classmethod_name(self):
    
    # Make a regex for what are acceptable method names.
    aceptable_methodnames = re.compile('^(' + '(\_)?' + Test_CodingStyle.SNAKE_CASE_REGEX + 
                                        '|' + '\_\_' + Test_CodingStyle.SNAKE_CASE_REGEX + '\_\_' +
                                        ')$')
    # Predicate to decide what's a method.
    method_predicate = lambda x : i.ismethod(x) or i.isfunction(x)
    
    # Get all global methods.
    global_methodnames = [name for name, member in i.getmembers(mxk) if method_predicate(member)]
    
    # Check 'em.
    self._check_names(global_methodnames, aceptable_methodnames)
    
    # Get all mxk classes.
    classes = [member for name, member in i.getmembers(mxk) if i.isclass(member)]
    
    for class_ in classes:
      
      # Get all method names in class_
      class_methodnames = [name for name, member in i.getmembers(class_, predicate=method_predicate)]
      
      # Check 'em.
      self._check_names(class_methodnames, aceptable_methodnames)
        

                                    

