import expr
import json
import utils

class PropUtils(object):
  
  @staticmethod
  def read_from_string(string):
    return PropUtils.read_from_object(json.loads(string))
  
  @staticmethod
  def read_from_object(obj):
    
    
    if type(obj) == dict:
      if len(obj.keys()) == 1:

        KEY = obj.keys()[0]
        VALUE = obj[KEY]
        TYPENAME = utils.Utils.underscore_to_camel_case(KEY)
        
        Type = getattr(expr, TYPENAME)
        
        if TYPENAME == "Var":
          return expr.Var(VALUE)
        elif TYPENAME == "Const":
          return expr.Const(VALUE)
        else:
          print str(Type)
          return Type([PropUtils.read_from_object(c) for c in VALUE])
        
        #return Type([transform(c) for c in obj[obj.keys()[0]]])
        
        #if obj.keys()[0] == "and":
        #  return expr.And
      else:
        raise Exception("Too many keys in {obj}".format(obj=obj))
    else:
      raise Exception("Unable to process object of type {type}".format(type=type(obj)))
        




 
import unittest

class Tests(unittest.TestCase):
  
  def test_parse_string(self):
    
    print PropUtils.read_from_string("""
      { "and" : "blah" } """)
      
    """
    
    [
        { "const" : true },  
        { "var" : '1' } 
      ]
    }"""