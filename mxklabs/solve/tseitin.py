import collections

from mxklabs.expr import expr as ex
from mxklabs.expr import exprbool as eb
from mxklabs.expr import exprtype as et
from mxklabs.expr import exprwalker as ew

from mxklabs import dimacs

class Tseitin(ew.Visitor):

  TRUE_LIT  = 1
  FALSE_LIT = -1
  
  def __init__(self):
    super().__init__()

    # Map ids to literals.
    self._idcache = \
    { 
      ex.Constant(type=et.Bool(), value=True) : Tseitin.TRUE_LIT,
      ex.Constant(type=et.Bool(), value=False) : Tseitin.FALSE_LIT 
    }
    self._dimacs = dimacs.Dimacs(clauses=set([frozenset([Tseitin.TRUE_LIT])]))

  def dimacs(self):
    return self._dimacs
  
  ''' Evaluate a boolean expression and ensure it is asserted to hold. '''
  def add_constraint(self, expr):
    if isinstance(expr, eb.LogicalAnd):
      for child in expr.children():
        self.add_constraint(child)
    else:    
      lit = self.bottom_up_walk(expr)
      self._dimacs.clauses.add(frozenset([lit]))
    
  ''' Evaluate a number of boolean expressions and ensure they are asserted. '''
  def add_constraints(self, exprs):
    for expr in exprs:
      self.add_constraint(expr)   
  
  ''' Return a representation of this expression in the form of literals. '''
  def visit_variable(self, expr, args):
    if expr.type() == et.Bool():
      lit = self._lit(expr)
      return lit
    else:
      raise RuntimeError("type {type} not supported".format(type=type))

  ''' Return a representation of this expression in the form of literals. '''
  def visit_constant(self, expr, args):    
    if expr.type() == et.Bool():
      # True and false are in the cache (see __init__).
      lit = self._lit(expr)
      return lit
    else:
      raise RuntimeError("type {type} not supported".format(type=type))

  def visit_logical_and(self, expr, args):
    exprlit, fresh = self._lit_with_flag(expr)
    
    if fresh:
      # Ensure when the logical and is true, exprlit is true.
      self._dimacs.clauses.add(frozenset([exprlit]+[-args[child] for child in expr.children()]))
      
      # Ensure when any child causes the logical and to be false, exprlit is false, too.
      for child in expr.children():
        childlit = args[child]
        self._dimacs.clauses.add(frozenset([-exprlit, childlit]))
    
    return exprlit
  
  def visit_logical_or(self, expr, args):
    exprlit, fresh = self._lit_with_flag(expr)
    
    if fresh:
      # Ensure when the logical or is false, exprlit is false.
      self._dimacs.clauses.add(frozenset([-exprlit]+[args[child] for child in expr.children()]))
      
      # Ensure when any child causes the logical and to be true, exprlit is true, too.
      for child in expr.children():
        childlit = args[child]
        self._dimacs.clauses.add(frozenset([exprlit, -childlit]))
    
    return exprlit
  
  def visit_logical_not(self, expr, args):
    return -args[expr.child()]
  
  ''' Generate a literal. '''
  def _lit(self, expr):
    if expr not in self._idcache.keys():
      self._dimacs.num_vars += 1
      self._idcache[expr] = self._dimacs.num_vars

    return self._idcache[expr]
  
  ''' Generate a literal. '''
  def _lit_with_flag(self, expr):
    if expr not in self._idcache.keys():
      self._dimacs.num_vars += 1
      self._idcache[expr] = self._dimacs.num_vars
      return (self._idcache[expr], True)
    else:
      return (self._idcache[expr], False)
  
  ''' Helper function to escape strings. '''
  def _escape(self, string):    
    return string.replace('$', '$$')
  
  ''' Print cache. '''
  def _print_cache(self):
    for exprstr, lit in self._idcache.items():
      print("'{exprstr}' -> {lit}".format(exprstr=exprstr, lit=lit))
