import collections

from mxklabs.expr import expr as e

''' Help eliminate constants in expressions. '''

class ConstProp(e.Visitor):
  
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
      return ConstProp.Res(expr=e.Const(e.Bool, False), is_const=True, value=False)
    
    # If ALL operands are true, return true.
    if all([args[child].is_const and args[child].value for child in expr.children()]):
      return ConstProp.Res(expr=e.Const(e.Bool, True), is_const=True, value=True)
    
    
    return ConstProp.Res(expr=expr, is_const=False, value=None)
  
  def visit_or(self, expr, args):
    return ConstProp.Res(expr=expr, is_const=False, value=None)
  
  def visit_not(self, expr, args):
    return ConstProp.Res(expr=expr, is_const=False, value=None)
  

  
