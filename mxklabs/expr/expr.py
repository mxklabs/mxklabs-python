import functools

import mxklabs.utils

from mxklabs.expr import exprtype as et

''' 
  Base class for all expression classes.  
'''
@functools.total_ordering
class Expression(object):
  
  def __init__(self, type, nodestr, children=[]):
    
    self._type = type
    self._children = children
    
    if len(children) == 0:
      self._hashstr = nodestr
    else:
      self._hashstr = "({nodestr} {children})".format(
        nodestr=nodestr,
        children=" ".join([o._hashstr for o in children]))

    if not et.isType(type):
        raise Exception("the 'type' parameter of expression '{expr}' must inherit from type 'Type' (found type " "'{type}')".format(expr=self, type=type.__class__.__name__))
    
    try:
      it = iter(self._children)
    except:
      raise Exception("the 'children' parameter must be a iterable collection of 'Expression' objects")
    
    for child in self._children:
      if not isExpression(child):
        raise Exception("the 'children' parameter must be a iterable collection of 'Expression' objects")

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
    return et.Product([c.codomain() for c in self.children()])
    
  def codomain(self):
    return self._type
  
  def visit(self, visitor, args):
    visit_method_name = 'visit_' + mxklabs.utils.Utils.camel_case_to_underscore(type(self).__name__)
    visit_method = getattr(visitor, visit_method_name)
    return visit_method(self, args)
  
  ''' Work out the value of the expression given a map from self.children to values. '''
  def evaluate(self, args):
    raise Exception("Not implemented for class {classname}".format(classname=self.__class__.__name__))

  def ensureNumberOfChildren(self, n):
    if len(self._children) != n:
      raise Exception("type \"{type}\" requires exactly {num_children} operand(s)".format(
                      type=type(self), num_children=n))
 
  def ensureMinimumNumberOfChildren(self, n):
    if len(self._children) < n:
      raise Exception("type \"{type}\" requires at least {min_num_children} operand(s)".format(
                      type=type(self), min_num_children=n))
    
  def ensureMaximumNumberOfChildren(self, n):
    if len(self._children) > n:
      raise Exception("type \"{type}\" requires at most {max_num_children} operand(s)".format(
                      type=type(self), max_num_children=n))

  def ensureChildIsConstant(self, index):
    if not isinstance(self._children[index], Constant):
      raise Exception("type \"{type}\" requires subexpression '{childstr}' to be constant".format(
                      type=type(self), childstr=str(self._children[index])))

  def ensureChildIsType(self, index, type):
    if self._children[index].type() != type:
      raise Exception("type \"{type}\" requires subexpression '{childstr}' to be to be of type "
                      "'{exptype}' but it is of type '{childtype}')".format(
                      type=type(self), childstr=str(self._children[index]), exptype=type, 
                      childtype=type(self._children[index])))

''' Helper function to decide if something is a subclass of Type. '''
def isExpression(expr):
  try:
    return isinstance(expr, Expression)
  except:
    return False


''' Constant. '''

class Constant(Expression):
  
  def __init__(self, type, value):
    Expression.__init__(self, type=type, nodestr="(const {value})".format(value=str(value).lower()))
    
    if not type.is_valid_value(value=value):
      raise Exception("'{value}' is not a valid value for a constant of type '{type}'".format(
                      value=value, type=type))

    self._value = value

  def evaluate(self, args):
    return self.value
  
  def value(self):
    return self._value

''' Variable. '''

class Variable(Expression):
  
  def __init__(self, type, id):
    Expression.__init__(self, type=type, nodestr="(var {id})".format(id=id))

    self.id = id
    
  def evaluate(self, args):
    return args[self]
  
''' Walker object. '''

class Visitor(object):
  
  def bottom_up_walk(self, expr):
    return expr.visit(self, dict([(c, self.bottom_up_walk(c)) for c in expr.children()]))
