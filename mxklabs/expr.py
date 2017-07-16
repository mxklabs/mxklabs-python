import functools

''' Base class for all types. '''
class Type(object):
  
  def __init__(self, type):
    self._type = type
    
  def __eq__(self, other):
    return self._type == other._type
  
  def __hash__(self):
    return hash(self._type)
  
''' Type constants. '''
Bool = Type("bool")

''' Base class for all expressions. '''
@functools.total_ordering
class Expression(object):
  
  def __init__(self, type, hashstr):
    self._type = type
    self._hashstr = hashstr

  def type(self):
    return self._type
  
  def __lt__(self, other):
    return self._hashstr < other._hashstr

  def __eq__(self, other):
    return self._hashstr == other._hashstr
  
  def __hash__(self):
    return hash(self._hashstr)

''' Variable. '''

class Variable(Expression):
  
  def __init__(self, id, type=Bool):
    Expression.__init__(self, type=type, hashstr="@{id}".format(id=id))
    self._id = id

''' Function. '''

class Function(Expression):
  
  def __init__(self, name, operands, type=Bool):
    Expression.__init__(self, type=type, hashstr="({name} {operands})".format(
      name=name,
      operands=" ".join([o._hashstr for o in operands])
    ))
    self._name = name
    self._operands = operands

''' Logical conjunction. '''
  
class LogicalAnd(Function):
  
  def __init__(self, operands):
    Function.__init__(self, name="and", operands=sorted(operands), type=Bool)
    
# 

#class Constant(Expr):
#  def __init__(self, type, value):
#    Expr.__init__(type=type, )
#  
#class Variable(Expr):

#class And(object):
  
#  def __init__(self, operands):
#    Expr.__init__(Bool, "and", operands)
#    self.operation = operation
#    self.operands = operands
#    self.type = type
  
#class Visitor(object):
  
#  def walk(expr, )
#  #
#    if expr.
  
class Walker(object):
  
  @staticmethod
  def walk_bottom_up(expr, visitor):
    
    t_children = [visitor(child) for child in expr.children()]
    t_expr = visitor.visit(expr, t_children)
    
    return t_expr  
    
    
         
  
  
import unittest

class Tests(unittest.TestCase):
  
  def test_expr_hashstr(self):    
    self.assertEquals(LogicalAnd([Variable("v1"),Variable("v2")])._hashstr, "(and @v1 @v2)")
    self.assertEquals(LogicalAnd([Variable("v2"),Variable("v1")])._hashstr, "(and @v1 @v2)")
    
