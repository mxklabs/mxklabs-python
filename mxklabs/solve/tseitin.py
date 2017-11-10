from __future__ import print_function

import collections

import six

from mxklabs.expr import expr as ex
from mxklabs.expr import exprbool as eb
from mxklabs.expr import exprtype as et
from mxklabs.expr import exprwalker as ew

from mxklabs import dimacs

class TseitinCache(object):

  LookupResult = collections.namedtuple('LookupResult', ['littup', 'cache_hit'])

  TRUE_LIT  = 1
  FALSE_LIT = -1

  def __init__(self):
    # Map tuple of expression and bit to literal.
    self._cache = \
    { 
      ex.Constant(type=et.Bool(), user_value=True) : { 0 : TseitinCache.TRUE_LIT },
      ex.Constant(type=et.Bool(), user_value=False) : { 0 : TseitinCache.FALSE_LIT }
    }
    self._dimacs = dimacs.Dimacs(clauses=set([frozenset([TseitinCache.TRUE_LIT])]))

  def dimacs(self):
    return self._dimacs

  ''' Test to see if bit is cached. '''
  def is_cached(self, expr, bit=None):
    if bit is not None:
      return expr in self._cache.keys() and bit in self._cache[expr].keys()
    else:
      return all(self.is_cached(expr, bit) for bit in range(expr.type().littup_size()))

  ''' Lookup (returns just a literal number by default, or a LookupResult if specified. '''
  def lookup_lit(self, expr, bit):
    if expr not in self._cache.keys():
      self._dimacs.num_vars += 1
      self._cache[expr] = { bit : self._dimacs.num_vars }
      return self._dimacs.num_vars
    elif bit not in self._cache[expr]:
      self._dimacs.num_vars += 1
      self._cache[expr][bit] = self._dimacs.num_vars
    else:
      return self._cache[expr][bit]
    
  ''' Lookup (returns just a literal number by default, or a LookupResult if specified. '''
  def lookup_littup(self, expr):
    return tuple(self.lookup_lit(expr, bit) for bit in range(expr.type().littup_size()))
    
  ''' Add a CNF clause. ''' 
  def add_clause(self, clause):
    self._dimacs.clauses.add(clause)

  ''' Print cache. '''
  def print(self):
    for exprstr, lit in self._cache.items():
      print("'{exprstr}:{bit}' -> {lit}".format(exprstr=exprstr, lit=lit))


class Tseitin(ew.Visitor):
  
  def __init__(self):
    self._cache = TseitinCache()
    super().__init__()
  
  def dimacs(self):
    return self._cache.dimacs()
  
  ''' Evaluate a boolean expression and ensure it is asserted to hold. '''
  def add_constraint(self, expr):
    if isinstance(expr, eb.LogicalAnd):
      # This is a small optimisation (avoid additional literals).
      for child in expr.children():
        self.add_constraint(child)
    elif expr.type() == et.Bool():    
      littup = self.bottom_up_walk(expr)
      lit, = self.bottom_up_walk(expr)
      self._cache.add_clause(frozenset([lit]))
    else:
      raise("Cannot add an expression with type '{type_}' as a constraint".format(type_=expr.type()))
    
  ''' Evaluate a number of boolean expressions and ensure they are asserted. '''
  def add_constraints(self, exprs):
    for expr in exprs:
      self.add_constraint(expr)
      
  ''' Can be used to established what literals belong to an expression. '''  
  def cache_lookup(self, expr):
    return self._cache.lookup_littup(expr)

  def _memoise(self, impl, expr, res):
    if self._cache.is_cached(expr):
      return self._cache.lookup_littup(expr)
    else:
      return impl(expr, res)
  
  ''' Return a representation of this expression in the form of literals. '''
  def visit_variable(self, expr, res, args):
    return self._cache.lookup_littup(expr)

  ''' Return a representation of this expression in the form of literals. '''
  def visit_constant(self, expr, res, args):
    return tuple(TseitinCache.TRUE_LIT if valbit else TseitinCache.FALSE_LIT for valbit in expr.value().littup_value())

  ''' Return a representation of this expression in the form of literals. '''
  def visit_logical_and(self, expr, res, args):

    def impl(expr, res):

      littup = self._cache.lookup_littup(expr)
      lit, = littup
    
      # Ensure when the logical and is true, exprlit is true.
      self._cache.add_clause(frozenset([lit]+[-res[child][0] for child in expr.children()]))
      
      # Ensure when any child causes the logical and to be false, exprlit is false, too.
      for child in expr.children():
        childlit = res[child][0]
        self._cache.add_clause(frozenset([-lit, childlit]))
        
      return littup
    
    return self._memoise(impl, expr, res)
  
  ''' Return a representation of this expression in the form of literals. '''
  def visit_logical_or(self, expr, res, args):

    def impl(expr, res):

      littup = self._cache.lookup_littup(expr)
      lit, = littup
      
      # Ensure when the logical or is false, exprlit is false.
      self._cache.add_clause(frozenset([-lit]+[res[child][0] for child in expr.children()]))
      
      # Ensure when any child causes the logical and to be true, exprlit is true, too.
      for child in expr.children():
        childlit = res[child][0]
        self._cache.add_clause(frozenset([lit, -childlit]))
        
      return littup
    
    return self._memoise(impl, expr, res)
  
  def visit_logical_not(self, expr, res, args):
    return (-res[expr.child()][0],)
