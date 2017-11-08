import collections

from mxklabs.expr import exprtype as et
from mxklabs.expr import expr as ex
from mxklabs.expr import exprwalker as ew


''' Help eliminate constants in expressions. '''

class VariableHarvester(ew.Visitor):
  
  Res = collections.namedtuple('Res', ['vars'])
  
  def _process(self, expr):
    return self.bottom_up_walk(expr).vars
  
  def visit_constant(self, expr, args):
    return self.visit_default(expr, args)
  
  def visit_variable(self, expr, args):
    return VariableHarvester.Res(vars=set([expr]))
  
  def visit_logical_and(self, expr, args):
    return self.visit_default(expr, args)
  
  def visit_logical_or(self, expr, args):
    return self.visit_default(expr, args)
  
  def visit_logical_not(self, expr, args):
    return self.visit_default(expr, args)
  
  def visit_default(self, expr, args):
    
    result = set()
    
    for child in expr.children():
      result = result.union(args[child].vars)
  
    return VariableHarvester.Res(vars=result)
  
  ''' Quick version (avoid creating VariableHarvester). '''
  @staticmethod
  def process(expr):
    
    vh = VariableHarvester()
    return vh._process(expr)

''' Help eliminate constants in expressions. '''

class ConstantPropagator(ew.Visitor):
  
  Res = collections.namedtuple('Res', ['expr', 'is_const'])
  
  def _process(self, expr):
    return self.bottom_up_walk(expr).expr
  
  def visit_constant(self, expr, args):
    return ConstantPropagator.Res(expr=expr, is_const=True)
    
  def visit_variable(self, expr, args):
    return self.visit_default(expr, args)
  
  def visit_logical_and(self, expr, args):
    
    # If ANY operand is false, return falsex.
    if any([args[child].is_const and not args[child].expr.value()[0] for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(et.Bool(), (False,)), is_const=True)
    
    # If ALL operands are true, return truex.
    if all([args[child].is_const and args[child].expr.value()[0] for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(et.Bool(), (True,)), is_const=True)

    return ConstantPropagator.Res(expr=expr, is_const=False, value=None)
  
  def visit_logical_or(self, expr, args):
    
    # If ALL operand are false, return false.
    if all([args[child].is_const and not args[child].expr.value()[0] for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(et.Bool(), (False,)), is_const=True)
    
    # If ANY operand is true, return true.
    if any([args[child].is_const and args[child].expr.value()[0] for child in expr.children()]):
      return ConstantPropagator.Res(expr=ex.Constant(et.Bool(), (True,)), is_const=True)  

    return ConstantPropagator.Res(expr=expr, is_const=False)

  def visit_logical_not(self, expr, args):
    return self.visit_default(expr, args)
  
  def visit_default(self, expr, args):
    return ConstantPropagator.Res(expr=expr, is_const=False)
  
  ''' Quick version (avoid creating VariableHarvester). '''
  @staticmethod
  def process(expr):
    
    cp = ConstantPropagator()
    return cp._process(expr)
  
  ''' Help eliminate constants in expressions. '''

class ExpressionEvaluator(ew.Visitor):
  
  Res = collections.namedtuple('Res', ['expr', 'is_const'])
  
  def _process(self, expr):
    return self.bottom_up_walk(expr).expr
  
  def visit_constant(self, expr, args):
    return expr.value()
    
  def visit_variable(self, expr, args):
    return args[expr]
  
  def visit_logical_and(self, expr, args):
    return ev.ExprValue(type=et.Bool(), all(args[child].logical_value() for child in expr.children()]))
  
  def visit_logical_or(self, expr, args):
    return ev.ExprValue(type=et.Bool(), any(args[child].logical_value() for child in expr.children()]))

  def visit_logical_not(self, expr, args):
    return ev.ExprValue(type=et.Bool(), args[expr.child()].logical_value())
  
  ''' Quick version (avoid creating VariableHarvester). '''
  @staticmethod
  def process(expr):
    
    ee = ExpressionEvaluator()
    return ee._process(expr)

  
  