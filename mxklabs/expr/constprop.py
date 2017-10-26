import collections

''' Help eliminate constants in expressions. '''

class ConstProp(Visitor):
  
  Res = collections.namedtuple('Res', ['expr', 'is_const', 'value'])
  
  def process(self, expr):
    return self.bottom_up_walk(expr).expr
  
  def visit_var(self, expr, args):
    return ConstProp.Res(expr=expr, is_const=False, value=None)
  
  def visit_const(self, expr, args):
    return ConstProp.Res(expr=expr, is_const=True, value=expr.value)
  
  def visit_and(self, expr, args):
    
    # If ANY operand is false, return false.
    if any([args[child].is_const and not args[child].value for child in expr.children()]):
      return ConstProp.Res(expr=Const(Bool, False), is_const=True, value=False)
    
    # If ALL operands are true, return true.
    if all([args[child].is_const and args[child].value for child in expr.children()]):
      return ConstProp.Res(expr=Const(Bool, True), is_const=True, value=True)
    
    
    return ConstProp.Res(expr=expr, is_const=False, value=None)
  
  def visit_or(self, expr, args):
    return ConstProp.Res(expr=expr, is_const=False, value=None)
  
  def visit_not(self, expr, args):
    return ConstProp.Res(expr=expr, is_const=False, value=None)
  

import unittest

class Tests(unittest.TestCase):
  
  def test_and(self):              
    const_prop = ConstProp()
    
    # Check (and (var v1) (const false)) simplifies to (const false)
    self.assertEquals(
      Const(Bool, False), 
      const_prop.process(And([Var(Bool, "v1"),Const(Bool, False)])))

    # Check (and (var v1) (const false)) simplifies to (const false)
    self.assertEquals(
      Const(Bool, True), 
      const_prop.process(And([Const(Bool, True),Const(Bool, True)])))
  
