import collections

from mxklabs.expr import exprtype as et
from mxklabs.expr import expr as ex
from mxklabs.expr import exprwalker as ew

''' Help eliminate constants in expressions. '''

class ConstProp(ew.Visitor):
  
  Res = collections.namedtuple('Res', ['expr', 'is_const', 'value'])
  
  def process(self, expr):
    return self.bottom_up_walk(expr).expr
  
  def visit_variable(self, expr, args):
    return ConstProp.Res(expr=expr, is_const=False, value=None)
  
  def visit_constant(self, expr, args):
    return ConstProp.Res(expr=expr, is_const=True, value=expr.value())
  
  def visit_logical_and(self, expr, args):
    
    # If ANY operand is false, return falsex.
    if any([args[child].is_const and not args[child].value for child in expr.children()]):
      return ConstProp.Res(expr=ex.Constant(et.Bool(), False), is_const=True, value=False)
    
    # If ALL operands are true, return truex.
    if all([args[child].is_const and args[child].value for child in expr.children()]):
      return ConstProp.Res(expr=ex.Constant(et.Bool(), True), is_const=True, value=True)

    return ConstProp.Res(expr=expr, is_const=False, value=None)
  
  def visit_logical_or(self, expr, args):
    
    # If ALL operand are false, return false.
    if all([args[child].is_const and not args[child].value for child in expr.children()]):
      return ConstProp.Res(expr=ex.Constant(et.Bool(), False), is_const=True, value=False)
    
    # If ANY operand is true, return true.
    if any([args[child].is_const and args[child].value for child in expr.children()]):
      return ConstProp.Res(expr=ex.Constant(et.Bool(), True), is_const=True, value=True)  

    return ConstProp.Res(expr=expr, is_const=False, value=None)

  def visit_logical_not(self, expr, args):
    return ConstProp.Res(expr=expr, is_const=False, value=None)
  

  
  