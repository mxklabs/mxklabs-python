import collections

from mxklabs.expr import exprtype as et
from mxklabs.expr import expr as ex
from mxklabs.expr import exprwalker as ew


''' Help eliminate constants in expressions. '''

class VariableHarvester(ew.Visitor):
  
  Res = collections.namedtuple('Res', ['vars'])
  
  def process(self, expr):
    return self.bottom_up_walk(expr).vars
  
  def visit_variable(self, expr, args):
    return VariableHarvester.Res(vars=set([expr]))
  
  def visit_default(self, expr, args):
    
    result = set()
    
    for child in expr.children():
      result = result.union(args[child].vars)
  
    return VariableHarvester.Res(vars=result)
  
''' Quick version (avoid creating VariableHarvester). '''
def harvest_variables(expr):
    
    vh = VariableHarvester()
    return vh.process(expr)

''' Help eliminate constants in expressions. '''

class ConstantPropagator(ew.Visitor):
  
  Res = collections.namedtuple('Res', ['expr', 'is_const', 'value'])
  
  def process(self, expr):
    return self.bottom_up_walk(expr).expr
  
  def visit_constant(self, expr, args):
    return ConstantPropagator.Res(expr=expr, is_const=True, value=expr.value())
  
  def visit_logical_and(self, expr, args):
    
    # If ANY operand is false, return falsex.
    if any([args[child].is_const and not args[child].value for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(et.Bool(), False), is_const=True, value=False)
    
    # If ALL operands are true, return truex.
    if all([args[child].is_const and args[child].value for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(et.Bool(), True), is_const=True, value=True)

    return ConstantPropagator.Res(expr=expr, is_const=False, value=None)
  
  def visit_logical_or(self, expr, args):
    
    # If ALL operand are false, return false.
    if all([args[child].is_const and not args[child].value for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(et.Bool(), False), is_const=True, value=False)
    
    # If ANY operand is true, return true.
    if any([args[child].is_const and args[child].value for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(et.Bool(), True), is_const=True, value=True)  

    return ConstantPropagator.Res(expr=expr, is_const=False, value=None)

  def visit_default(self, expr, args):
    return ConstantPropagator.Res(expr=expr, is_const=False, value=None)
  
''' Quick version (avoid creating VariableHarvester). '''
def propagate_constants(expr):
    
    cp = ConstantPropagator()
    return cp.process(expr)

  
  