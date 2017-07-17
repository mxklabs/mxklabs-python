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

''' Constant. '''

class Constant(Expression):
  
  def __init__(self, value, type=Bool):
    Expression.__init__(self, type=type, hashstr="(value {value})".format(value=str(value).lower()))
    self._value = value
    
''' Variable. '''

class Variable(Expression):
  
  def __init__(self, id, type=Bool):
    Expression.__init__(self, type=type, hashstr="(var {id})".format(id=id))
    self._id = id

''' Function. '''

class Function(Expression):
  
  def __init__(self, name, operands, type=Bool, num_operands=None, min_num_operands=None, max_num_operands=None):
    Expression.__init__(self, type=type, hashstr="({name} {operands})".format(
      name=name,
      operands=" ".join([o._hashstr for o in operands])
    ))
    self._name = name
    self._operands = operands
    self._num_operands = num_operands
    self._min_num_operands = min_num_operands
    self._max_num_operands = max_num_operands
    
    self.check()
  
  def check(self):
    
    if self._num_operands is not None and len(self._operands) != self._num_operands:
      raise Exception("type \"{type}\" requires exactly {num_operands} operand(s)".format(
        type=type(self), 
        num_operands=self._num_operands
      ))

    if self._min_num_operands is not None and len(self._operands) < self._min_num_operands:
      raise Exception("type \"{type}\" requires at least {min_num_operands} operand(s)".format(
        type=type(self), 
        min_num_operands=self._min_num_operands
      ))
    
    if self._max_num_operands is not None and len(self._operands) > self._max_num_operands:
      raise Exception("type \"{type}\" requires at most {max_num_operands} operand(s)".format(
        type=type(self), 
        max_num_operands=self._max_num_operands
      ))
''' Logical operations. '''
  
class LogicalAnd(Function):
  
  def __init__(self, operands):
    Function.__init__(self, name="and", operands=sorted(operands), type=Bool, min_num_operands=1)

class LogicalOr(Function):
  
  def __init__(self, operands):
    Function.__init__(self, name="or", operands=sorted(operands), type=Bool, min_num_operands=1)

class LogicalNot(Function):
  
  def __init__(self, operands):
    Function.__init__(self, name="not", operands=operands, type=Bool, num_operands=1)
    
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
    self.assertEquals(LogicalAnd([Variable("v1", Bool),Variable("v2", Bool)])._hashstr, "(and (var v1) (var v2))")
    self.assertEquals(LogicalAnd([Variable("v1", Bool),Constant(True, Bool)])._hashstr, "(and (value true) (var v1))")
    self.assertEquals(LogicalAnd([Variable("v2", Bool),Variable("v1", Bool)])._hashstr, "(and (var v1) (var v2))")
    self.assertEquals(LogicalOr([Constant(False, Bool),Variable("v1", Bool)])._hashstr, "(or (value false) (var v1))")
    
