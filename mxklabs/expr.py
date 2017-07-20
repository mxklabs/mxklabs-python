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
  
  def __str__(self):
    return self._hashstr  
  
  def __repr__(self):
    return self._hashstr

  def children(self):
    return self._children
  
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
    return visitor.visitConst(self, args)#
  
  def value(self):
    return self._value  
  
''' Variable. '''

class Var(Expression):
  
  def __init__(self, type, id):
    Expression.__init__(self, type=type, nodestr="(var {id})".format(id=id))
    self._id = id

  def visit(self, visitor, args):
    return visitor.visitVar(self, args)
    
  def id(self):
    return self._id

'''  operations. '''
  
class And(Expression):
  
  def __init__(self, children):
    Expression.__init__(self, type=Bool, nodestr="and", children=children, min_num_children=1)
    
  def visit(self, visitor, args):
    return visitor.visitAnd(self, args)

class Or(Expression):
  
  def __init__(self, children):
    Expression.__init__(self, type=Bool, nodestr="or", children=children, min_num_children=1)
    
  def visit(self, visitor, args):
    return visitor.visitOr(self, args)

class Not(Expression):
  
  def __init__(self, children):
    Expression.__init__(self, type=Bool, nodestr="not", children=children, num_children=1)

  def visit(self, visitor, args):
    return visitor.visitNot(self, args)

  
''' Visitor object. '''
  
class Visitor(object):

  @abc.abstractmethod
  def visitVar(self, expr, args): pass

  @abc.abstractmethod
  def visitConst(self, expr, args): pass

  @abc.abstractmethod
  def visitAnd(self, expr, args): pass

  @abc.abstractmethod
  def visitOr(self, expr, args): pass

  @abc.abstractmethod
  def visitNot(self, expr, args): pass

''' Walker object. '''
  
class Walker(object):
  
  def walk(self, expr, visitor):
    assert(isinstance(visitor, Visitor))
    return expr.visit(visitor, dict([(c, self.walk(c, visitor)) for c in expr.children()]))  
  
import unittest

class Tests(unittest.TestCase):
  
  def test_expr_hashstr(self):    
    self.assertEquals(And([Var(Bool, "v1"),Var(Bool, "v2")])._hashstr, "(and (var v1) (var v2))")
    self.assertEquals(And([Var(Bool, "v1"),Const(Bool, True)])._hashstr, "(and (var v1) (const true))")
    self.assertEquals(And([Var(Bool, "v2"),Var(Bool, "v1")])._hashstr, "(and (var v2) (var v1))")
    self.assertEquals(Or([Const(Bool, False),Var(Bool, "v1")])._hashstr, "(or (const false) (var v1))")
    
  def test_expr_walker(self):
    
    class PrettyPrinter(Visitor):
      
      def visitVar(self, expr, args): 
        return str(expr.id())
      
      def visitConst(self, expr, args): 
        return str(expr.value()).lower()
      
      def visitAnd(self, expr, args):
        return "(" + " AND ".join([args[c] for c in expr.children()]) + ")"
      
      def visitOr(self, expr, args): 
        return "(" + " OR ".join([args[c] for c in expr.children()]) + ")"
      
      def visitNot(self, expr, args): 
        return "(NOT" + args[expr.children()[0]] + ")"
    
    expr = And([Var(Bool, "v1"),Or([Const(Bool, False),Var(Bool, "v1")])])
    visitor = PrettyPrinter()
    walker = Walker()
    
    self.assertEquals(walker.walk(expr, visitor), "(v1 AND (false OR v1))")
    
  
    
