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

class VariableHarvester(ExprWalker):
  
  Res = collections.namedtuple('Res', ['vars'])
  
  def _process(self, expr):
    return self.bottom_up_walk(expr=expr, args=None).vars
  
  def visit_constant(self, expr, res, args):
    return self.visit_default(expr, res, args)
  
  def visit_variable(self, expr, res, args):
    return VariableHarvester.Res(vars=set([expr]))
  
  def visit_logical_and(self, expr, res, args):
    return self.visit_default(expr, res, args)
  
  def visit_logical_or(self, expr, res, args):
    return self.visit_default(expr, res, args)
  
  def visit_logical_not(self, expr, res, args):
    return self.visit_default(expr, res, args)
  
  def visit_default(self, expr, res, args):
    
    result = set()
    
    for child in expr.children():
      result = result.union(res[child].vars)
  
    return VariableHarvester.Res(vars=result)
  
  ''' Quick version (avoid creating VariableHarvester). '''
  @staticmethod
  def process(expr):
    
    vh = VariableHarvester()
    return vh._process(expr)

''' Help propagate constant expressions. '''

class ConstantPropagator(ExprWalker):
  
  Res = collections.namedtuple('Res', ['expr', 'is_const'])
  
  def _process(self, expr):
    return self.bottom_up_walk(expr=expr, args=None).expr
  
  def visit_constant(self, expr, res, args):
    return ConstantPropagator.Res(expr=expr, is_const=True)
    
  def visit_variable(self, expr, res, args):
    return self.visit_default(expr, res, args)
  
  def visit_logical_and(self, expr, res, args):
    
    # If ANY operand is false, return falsex.
    if any([res[child].is_const and not res[child].expr.value().user_value() for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(type='bool', user_value=False), is_const=True)
    
    # If ALL operands are true, return truex.
    if all([res[child].is_const and res[child].expr.value().user_value() for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(type='bool', user_value=True), is_const=True)

    return ConstantPropagator.Res(expr=expr, is_const=False, value=None)
  
  def visit_logical_or(self, expr, res, args):
    
    # If ALL operand are false, return false.
    if all([res[child].is_const and not res[child].expr.value().user_value() for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(type='bool', user_value=False), is_const=True)
    
    # If ANY operand is true, return true.
    if any([res[child].is_const and res[child].expr.value().user_value() for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(type='bool', user_value=True), is_const=True)

    return ConstantPropagator.Res(expr=expr, is_const=False)

  def visit_logical_not(self, expr, res, args):
    return self.visit_default(expr, res, args)
  
  def visit_default(self, expr, res, args):
    return ConstantPropagator.Res(expr=expr, is_const=False)
  
  ''' Quick version (avoid creating VariableHarvester). '''
  @staticmethod
  def process(expr):
    
    cp = ConstantPropagator()
    return cp._process(expr)
  
''' Evaluate the value of an expressions. '''

class ExpressionEvaluator(ExprWalker):
  
  def _process(self, expr, variable_value_map):
    return self.bottom_up_walk(expr=expr, args=variable_value_map)
  
  def visit_constant(self, expr, res, args):
    return expr.value()
    
  def visit_variable(self, expr, res, args):
    return args[expr]
  
  def visit_logical_and(self, expr, res, args):
    return et.ExprValue(type=et.Bool(), user_value=all([res[child].user_value() for child in expr.children()]))
  
  def visit_logical_or(self, expr, res, args):
    return et.ExprValue(type=et.Bool(), user_value=any([res[child].user_value() for child in expr.children()]))

  def visit_logical_not(self, expr, res, args):
    return et.ExprValue(type=et.Bool(), user_value=not res[expr.child()].user_value())
  
  ''' Quick version (avoid creating VariableHarvester). '''
  @staticmethod
  def process(expr, variable_value_map):
    
    ee = ExpressionEvaluator()
    return ee._process(expr, variable_value_map)

  
  