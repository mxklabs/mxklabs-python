import functools

import mxklabs.utils

from mxklabs.expr import exprtype as et

''' Base class for all expression classes. '''

@functools.total_ordering
class Expr(object):
  
  def __init__(self, type, nodestr, children=[]):
    
    self._type = type
    self._children = children
    
    if len(children) == 0:
      self._hash_str = nodestr
    else:
      self._hash_str = "({nodestr} {children})".format(
        nodestr=nodestr,
        children=" ".join([o._hash_str for o in children]))

    if not et.ExprType.is_exprtype(type):
        raise Exception("the 'type' parameter of expression '{expr}' must inherit from type 'ExprType' (found type " "'{type}')".format(expr=self, type=type.__class__.__name__))
    
    try:
      it = iter(self._children)
    except:
      raise Exception("the 'children' parameter must be a iterable collection of 'Expr' objects")
    
    for child in self._children:
      if not Expr.is_expr(child):
        raise Exception("the 'children' parameter must be a iterable collection of 'Expr' objects")

  def type(self):
    return self._type
  
  def hash_str(self):
    return self._hash_str
  
  def __lt__(self, other):
    return self._hash_str < other._hash_str

  def __eq__(self, other):
    return self._hash_str == other._hash_str
  
  def __hash__(self):
    return hash(self._hash_str)
  
  def __str__(self):
    return self._hash_str  
  
  def __repr__(self):
    return self._hash_str

  def child(self, index=0):
    return self._children[index]

  def children(self):
    return self._children
  
  def domain(self):
    return et.Product([c.codomain() for c in self.children()])
    
  def codomain(self):
    return self._type
  
  def visit(self, visitor, args):
    visit_method_name = 'visit_' + mxklabs.utils.Utils.camel_case_to_snake_case(type(self).__name__)
    visit_method = getattr(visitor, visit_method_name)
    result = visit_method(self, args)
    return result
  
  ''' Work out the value of the expression given a map from self.children to values. '''
  def evaluate(self, args):
    raise Exception("Not implemented for class {classname}".format(classname=self.__class__.__name__))

  def ensure_number_of_children(self, n):
    if len(self._children) != n:
      raise Exception("type \"{type}\" requires exactly {num_children} operand(s)".format(
                      type=type(self), num_children=n))
 
  def ensure_minimum_number_of_children(self, n):
    if len(self._children) < n:
      raise Exception("type \"{type}\" requires at least {min_num_children} operand(s)".format(
                      type=type(self), min_num_children=n))
    
  def ensure_maximum_number_of_children(self, n):
    if len(self._children) > n:
      raise Exception("type \"{type}\" requires at most {max_num_children} operand(s)".format(
                      type=type(self), max_num_children=n))

  def ensure_child_is_constant(self, index):
    if not isinstance(self._children[index], Constant):
      raise Exception("type \"{type}\" requires subexpression '{childstr}' to be constant".format(
                      type=type(self), childstr=str(self._children[index])))

  def ensure_child_is_type(self, index, type):
    if self._children[index].type() != type:
      raise Exception("type \"{type}\" requires subexpression '{childstr}' to be to be of type "
                      "'{exptype}' but it is of type '{childtype}')".format(
                      type=type(self), childstr=str(self._children[index]), exptype=type, 
                      childtype=type(self._children[index])))

  ''' Helper function to decide if something is a subclass of ExprType. '''
  @staticmethod
  def is_expr(expr):
    try:
      return isinstance(expr, Expr)
    except:
      return False
  
''' Constant. '''

class Constant(Expr):
  
  def __init__(self, type, value):
    Expr.__init__(self, type=type, nodestr="(const {value})".format(value=str(value).lower()))
    
    if not type.is_valid_value(value=value):
      raise Exception("'{value}' is not a valid value for a constant of type '{type}'".format(
                      value=value, type=type))

    self._value = value

  def evaluate(self, args):
    return self.value
  
  def value(self):
    return self._value

''' Variable. '''

class Variable(Expr):
  
  def __init__(self, type, id):
    Expr.__init__(self, type=type, nodestr="(var {id})".format(id=id))

    self.id_ = id
    
  def evaluate(self, args):
    return args[self]

  def id(self):
    return self.id_
  
''' Walker object. '''

class Visitor(object):
  
  def bottom_up_walk(self, expr):
    return expr.visit(self, dict([(c, self.bottom_up_walk(c)) for c in expr.children()]))
