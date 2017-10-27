import abc
import functools
import itertools
import six

import mxklabs.utils

''' Simple type. '''
class Type(object):
  
  def __init__(self, typestr, values, num_values):
    
    self._typestr = typestr
    self._values = values
    self._num_values = num_values
    
  def __eq__(self, other):
    return self._typestr == other._typestr
  
  def __hash__(self):
    return hash(self._typestr)
  
  def __str__(self):
    return self._typestr  
  
  def __repr__(self):
    return self._typestr
  
  def values(self):
    return self._values
  
  def num_values(self):
    return self._num_values
  
''' Product of types. '''
class Product(Type):
  
  def __init__(self, subtypes):
    
    Type.__init__(self, 
      typestr="(" + ",".join([t._typestr for t in subtypes]) + ")",
      values=itertools.product(*[t.values() for t in subtypes]),
      num_values=functools.reduce(lambda x, y : (x.num_values() if isinstance(x, Type) else x)  * y.num_values(), subtypes))
    
    self.subtypes = subtypes
    
''' Unparameterised types. '''

Bool = Type("bool", values=[False,True], num_values=2)

''' 
  Base class for all expression classes.  
'''
@functools.total_ordering
class Expression(object):
  
  def __init__(self, type, nodestr, children=[], num_children=None, min_num_children=None, max_num_children=None):
    
    self._type = type
    self._children = children
    self._num_children = num_children
    self._min_num_children = min_num_children
    self._max_num_children = max_num_children
    
    if len(children) == 0:
      self._hashstr = nodestr
    else:
      self._hashstr = "({nodestr} {children})".format(
        nodestr=nodestr,
        children=" ".join([o._hashstr for o in children]))

    self._check()

  def type(self):
    return self._type
  
  def __lt__(self, other):
    return self._hashstr < other._hashstr

  def __eq__(self, other):
    return self._hashstr == other._hashstr
  
  def __hash__(self):
    return hash(self._hashstr)
  
  def __str__(self):
    return self._hashstr  
  
  def __repr__(self):
    return self._hashstr

  def children(self):
    return self._children
  
  def domain(self):
    return Product([c.codomain() for c in self.children()])
    
  def codomain(self):
    return self._type
  
  def visit(self, visitor, args):
    visit_method_name = 'visit_' + mxklabs.utils.Utils.camel_case_to_underscore(type(self).__name__)
    visit_method = getattr(visitor, visit_method_name)
    return visit_method(self, args)
  
  def _check(self):
    
    if self._num_children is not None and len(self._children) != self._num_children:
      raise Exception("type \"{type}\" requires exactly {num_children} operand(s)".format(
        type=type(self), 
        num_children=self._num_children))

    if self._min_num_children is not None and len(self._children) < self._min_num_children:
      raise Exception("type \"{type}\" requires at least {min_num_children} operand(s)".format(
        type=type(self), 
        min_num_children=self._min_num_children))
    
    if self._max_num_children is not None and len(self._children) > self._max_num_children:
      raise Exception("type \"{type}\" requires at most {max_num_children} operand(s)".format(
        type=type(self), 
        max_num_children=self._max_num_children))

''' Constant. '''

class Const(Expression):
  
  def __init__(self, type, value):
    Expression.__init__(self, type=type, nodestr="(const {value})".format(value=str(value).lower()))
    self.value = value

  def evaluate(self, args):
    return self.value

''' Variable. '''

class Var(Expression):
  
  def __init__(self, type, id):
    Expression.__init__(self, type=type, nodestr="(var {id})".format(id=id))
    self.id = id
    
  def evaluate(self, args):
    return args[self]
''' Walker object. '''

class Visitor(object):
  
  def bottom_up_walk(self, expr):
    return expr.visit(self, dict([(c, self.bottom_up_walk(c)) for c in expr.children()]))
