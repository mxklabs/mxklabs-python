import abc
import functools
import exprtype
import utils



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
    return exprtype.Product([c.codomain() for c in self.children()])
    
  def codomain(self):
    return self._type
  
  def visit(self, visitor, args):
    visit_method_name = 'visit_' + utils.Utils.camel_case_to_underscore(type(self).__name__)
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

'''  operations. '''
  
class And(Expression):
  
  def __init__(self, children):
    Expression.__init__(self, type=exprtype.Bool, nodestr="and", children=children, min_num_children=1)
    
  def evaluate(self, args):
    return all([args[c] for c in self.children()])
    
class Or(Expression):
  
  def __init__(self, children):
    Expression.__init__(self, type=exprtype.Bool, nodestr="or", children=children, min_num_children=1)
    
  def evaluate(self, args):
    return any([args[c] for c in self.children()])

class Not(Expression):
  
  def __init__(self, children):
    Expression.__init__(self, type=exprtype.Bool, nodestr="not", children=children, num_children=1)
    
  def evaluate(self, args):
    return not args[self.children()[0]]

''' Walker object. '''

class Visitor(object):
  
  def bottom_up_walk(self, expr):
    return expr.visit(self, dict([(c, self.bottom_up_walk(c)) for c in expr.children()]))
 
import unittest

class Tests(unittest.TestCase):
  
  def test_expr_hashstr(self):    
    self.assertEquals(And([Var(exprtype.Bool, "v1"),Var(exprtype.Bool, "v2")])._hashstr, "(and (var v1) (var v2))")
    self.assertEquals(And([Var(exprtype.Bool, "v1"),Const(exprtype.Bool, True)])._hashstr, "(and (var v1) (const true))")
    self.assertEquals(And([Var(exprtype.Bool, "v2"),Var(exprtype.Bool, "v1")])._hashstr, "(and (var v2) (var v1))")
    self.assertEquals(Or([Const(exprtype.Bool, False),Var(exprtype.Bool, "v1")])._hashstr, "(or (const false) (var v1))")
    
  def test_expr_walker(self):
    
    class PrettyPrinter(Visitor):
      def to_string(self, expr): return self.bottom_up_walk(expr);
      
      def visit_var(self, expr, args): return str(expr.id)
      def visit_const(self, expr, args): return str(expr.value).lower()
      def visit_and(self, expr, args): return "(" + " AND ".join([args[c] for c in expr.children()]) + ")"
      def visit_or(self, expr, args): return "(" + " OR ".join([args[c] for c in expr.children()]) + ")"
      def visit_not(self, expr, args): return "(NOT" + args[expr.children()[0]] + ")"
    
    expr = And([Var(exprtype.Bool, "v1"),Or([Const(exprtype.Bool, False),Var(exprtype.Bool, "v1")])])
    printer = PrettyPrinter()
    
    
    self.assertEquals(printer.to_string(expr), "(v1 AND (false OR v1))")
    
    