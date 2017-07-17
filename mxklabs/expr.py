import abc
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
  
  @abc.abstractmethod
  def visit(self, visitor, args): pass  
  
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
    self._value = value

  def visit(self, visitor, args):
    visitor.visitConst(self, args)
    
''' Variable. '''

class Var(Expression):
  
  def __init__(self, type, id):
    Expression.__init__(self, type=type, nodestr="(var {id})".format(id=id))
    self._id = id

  def visit(self, visitor, args):
    visitor.visitVar(self, args)

'''  operations. '''
  
class And(Expression):
  
  def __init__(self, children):
    Expression.__init__(self, type=Bool, nodestr="and", children=sorted(children), min_num_children=1)
    
  def visit(self, visitor, args):
    visitor.visitAnd(self, args)

class Or(Expression):
  
  def __init__(self, children):
    Expression.__init__(self, type=Bool, nodestr="or", children=sorted(children), min_num_children=1)
    
  def visit(self, visitor, args):
    visitor.visitAnd(self, args)

class Not(Expression):
  
  def __init__(self, children):
    Expression.__init__(self, type=Bool, nodestr="not", children=children, num_children=1)

  def visit(self, visitor, args):
    visitor.visitNot(self, args)

  
''' Visitor object. '''
  
class Visitor(object):

  @abc.abstractmethod
  def visitVar(expr, args): pass

  @abc.abstractmethod
  def visitConst(expr, args): pass

  @abc.abstractmethod
  def visitAnd(expr, args): pass

  @abc.abstractmethod
  def visitOr(expr, args): pass

  @abc.abstractmethod
  def visitNot(expr, args): pass
  
# 

#class Constant(Expr):
#  def __init__(self, type, value):
#    Expr.__init__(type=type, )
#  
#class Variable(Expr):

#class And(object):
  
#  def __init__(self, children):
#    Expr.__init__(Bool, "and", children)
#    self.operation = operation
#    self.children = children
#    self.type = type
  
#class Visitor(object):
  
#  def walk(expr, )
#  #
#    if expr.
  
class BottomUpWalker(object):
  
  
  
  @staticmethod
  def walk(expr, visitor):
    
    child_map = dict([(child, walk(child, visitor)) for child in expr.children()])
    t_expr = expr.visit(visitor, child_map)
    
    return t_expr  
    
    
         
  
  
import unittest

class Tests(unittest.TestCase):
  
  def test_expr_hashstr(self):    
    self.assertEquals(And([Var(Bool, "v1"),Var(Bool, "v2")])._hashstr, "(and (var v1) (var v2))")
    self.assertEquals(And([Var(Bool, "v1"),Const(Bool, True)])._hashstr, "(and (const true) (var v1))")
    self.assertEquals(And([Var(Bool, "v2"),Var(Bool, "v1")])._hashstr, "(and (var v1) (var v2))")
    self.assertEquals(Or([Const(Bool, False),Var(Bool, "v1")])._hashstr, "(or (const false) (var v1))")
    
