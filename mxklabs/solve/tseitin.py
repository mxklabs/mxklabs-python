import collections

from mxklabs.expr import exprtype as et
from mxklabs.expr import expr as ex
from mxklabs.expr import exprwalker as ew

from mxklabs import dimacs

class Tseitin(ew.Visitor):

  Res = collections.namedtuple('Res', ['cnfvars', 'cnfclauses','link'])
  
  def __init__(self):
    super().__init__()

    # Map ids to literals.
    self._idcache = \
    { 
      str(ex.Constant(type=et.Bool(), value=True)) : 1,
      str(ex.Constant(type=et.Bool(), value=False)) : -1 
    }
    self._dimacs = dimacs.Dimacs([[1]])
    
  def dimacs(self):
    return self._dimacs
  
  def add_constraint(self, expr):
    lit = self.bottom_up_walk(expr)
    self._dimacs.clauses.append([lit])  
    
  
  def visit_variable(self, expr, args):

    if expr.type() == et.Bool():
      return self._genlit(expr.id())    
    else:
      raise RuntimeError("type {type} not supported".format(type=type))

  def visit_constant(self, expr, args):    
    if expr.type() == et.Bool():
      # True and false are in the cache (see __init__).
      return self._genlit(expr)        
    else:
      raise RuntimeError("type {type} not supported".format(type=type))

  def visit_logical_and(self, expr, args):
    
    pass

  ''' Get a literal.  '''
  def _genlit(self, expr):
    # Turn into escaped string.
    escaped_id = self._escape(str(expr))
    
    if escaped_id not in self._idcache.keys():
      self._dimacs.num_vars += 1
      self._idcache[escaped_id] = self._dimacs.num_vars

    return self._idcache[escaped_id]
  
  ''' Escape strings. '''
  def _escape(self, string):    
    
    return string.replace('$', '$$')
