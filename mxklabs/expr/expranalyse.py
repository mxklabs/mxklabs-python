import collections

from mxklabs.expr import expr as ex
from mxklabs.expr import exprtype as et
from mxklabs import utils

''' Walker object. '''
class ExprWalker(object):
  def __init__(self):
    pass
  
  def bottom_up_walk(self, expr, args=None):

    assert (isinstance(expr, ex.Expr))

    visit_method_name = 'visit_' + utils.Utils.camel_case_to_snake_case(
      expr.__class__.__name__)
    visit_method = getattr(self, visit_method_name)

    res = dict([(c, self.bottom_up_walk(c, args)) for c in expr.children()])

    return visit_method(expr=expr, res=res, args=args)

''' Help eliminate constants in expressions. '''

class VarHarvester(ExprWalker):
  """
  TODO: Document how to extend.
  """
  
  Res = collections.namedtuple('Res', ['vars'])
  
  def _process(self, expr):
    return self.bottom_up_walk(expr=expr, args=None).vars
  
  def visit_const(self, expr, res, args):
    return self.visit_default(expr, res, args)
  
  def visit_var(self, expr, res, args):
    return VarHarvester.Res(vars=set([expr]))
  
  def visit_logical_and(self, expr, res, args):
    return self.visit_default(expr, res, args)
  
  def visit_logical_or(self, expr, res, args):
    return self.visit_default(expr, res, args)
  
  def visit_logical_not(self, expr, res, args):
    return self.visit_default(expr, res, args)

  def visit_equals(self, expr, res, args):
    return self.visit_default(expr, res, args)

  def visit_default(self, expr, res, args):
    
    result = set()
    
    for child in expr.children():
      result = result.union(res[child].vars)
  
    return VarHarvester.Res(vars=result)
  
  ''' Quick version (avoid creating VarHarvester). '''
  @staticmethod
  def process(expr):
    
    vh = VarHarvester()
    return vh._process(expr)

''' Help propagate constant expressions. '''

class ConstProp(ExprWalker):
  
  Res = collections.namedtuple('Res', ['expr', 'is_const'])
  
  def _process(self, expr):
    return self.bottom_up_walk(expr=expr, args=None).expr
  
  def visit_const(self, expr, res, args):
    return ConstProp.Res(expr=expr, is_const=True)
    
  def visit_var(self, expr, res, args):
    return self.visit_default(expr, res, args)
  
  def visit_logical_and(self, expr, res, args):
    
    # If ANY operand is false, return falsex.
    if any([res[child].is_const and not res[child].expr.value().user_value() for child in expr.children()]):
      return ConstProp.Res(expr=ex.Const(expr_type='bool', user_value=False), is_const=True)
    
    # If ALL operands are true, return truex.
    if all([res[child].is_const and res[child].expr.value().user_value() for child in expr.children()]):
      return ConstProp.Res(expr=ex.Const(expr_type='bool', user_value=True), is_const=True)

    return ConstProp.Res(expr=expr, is_const=False, value=None)
  
  def visit_logical_or(self, expr, res, args):
    
    # If ALL operand are false, return false.
    if all([res[child].is_const and not res[child].expr.value().user_value() for child in expr.children()]):
      return ConstProp.Res(expr=ex.Const(expr_type='bool', user_value=False), is_const=True)
    
    # If ANY operand is true, return true.
    if any([res[child].is_const and res[child].expr.value().user_value() for child in expr.children()]):
      return ConstProp.Res(expr=ex.Const(expr_type='bool', user_value=True), is_const=True)

    return ConstProp.Res(expr=expr, is_const=False)

  def visit_logical_not(self, expr, res, args):
    return self.visit_default(expr, res, args)

  def visit_equals(self, expr, res, args):
    if all([res[child].is_const for child in expr.children()]):
      is_equal = (res[expr.child(0)].expr.value() == res[expr.child(1)].expr.value())
      return ConstProp.Res(expr=ex.Const(expr_type='bool', user_value=(is_equal)), is_const=True)
    elif expr.child(0) == expr.child(1):
      # If we're comparing an expression to itself, it must be true, right?
      return ConstProp.Res(expr=expr, is_const=True)
    else:
      return ConstProp.Res(expr=expr, is_const=False)
  
  def visit_default(self, expr, res, args):
    return ConstProp.Res(expr=expr, is_const=False)
  
  ''' Quick version (avoid creating VarHarvester). '''
  @staticmethod
  def process(expr):
    
    cp = ConstProp()
    return cp._process(expr)
  
''' Evaluate the value of an expressions. '''


  
  