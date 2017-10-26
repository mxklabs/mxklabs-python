import unittest

from mxklabs.expr import *

class _Tests(unittest.TestCase):
  
  def test_camel_case_to_underscore(self):
    self.assertEqual("this_is_camel_case", _camel_case_to_underscore("ThisIsCamelCase"))
  
  def test_dashed_to_camel_case(self):
    self.assertEqual("ThisIsCamelCase", _underscore_to_camel_case("this_is_camel_case"))
    
  def test_camel_case_to_dashed(self):
    self.assertEqual("this-is-camel-case", _camel_case_to_dashed("ThisIsCamelCase"))
    
  def test_dashed_to_camel_case(self):
    self.assertEqual("ThisIsCamelCase", _dashed_to_camel_case("this-is-camel-case"))

  def test_Bool(self):   
    T = Bool
    self.assertEqual("bool", str(T))
    self.assertEqual([False, True], [value for value in T.values()])
    self.assertEqual(2, T.num_values())
    
  def test_BitVector(self):    
    T = BitVector(3)
    self.assertEqual("uint3", str(T))
    self.assertEqual([0,1,2,3,4,5,6,7], [value for value in T.values()])
    self.assertEqual(8, T.num_values())
    
  def test_Product(self):    
    T = Product([BitVector(2),Bool])
    self.assertEqual("(uint2,bool)", str(T))
    self.assertEqual([(0, False), (0, True), (1, False), (1, True), (2, False), (2, True), (3, False), (3, True)], [value for value in T.values()])
    self.assertEqual(8, T.num_values())
  
  def test_expr_hashstr(self):    
    self.assertEqual(And([Var(Bool, "v1"),Var(Bool, "v2")])._hashstr, "(and (var v1) (var v2))")
    self.assertEqual(And([Var(Bool, "v1"),Const(Bool, True)])._hashstr, "(and (var v1) (const true))")
    self.assertEqual(And([Var(Bool, "v2"),Var(Bool, "v1")])._hashstr, "(and (var v2) (var v1))")
    self.assertEqual(Or([Const(Bool, False),Var(Bool, "v1")])._hashstr, "(or (const false) (var v1))")
    
  def test_expr_walker(self):
    
    class PrettyPrinter(Visitor):
      def to_string(self, expr): return self.bottom_up_walk(expr);
      
      def visit_var(self, expr, args): return str(expr.id)
      def visit_const(self, expr, args): return str(expr.value).lower()
      def visit_and(self, expr, args): return "(" + " AND ".join([args[c] for c in expr.children()]) + ")"
      def visit_or(self, expr, args): return "(" + " OR ".join([args[c] for c in expr.children()]) + ")"
      def visit_not(self, expr, args): return "(NOT" + args[expr.children()[0]] + ")"
    
    expr = And([Var(Bool, "v1"),Or([Const(Bool, False),Var(Bool, "v1")])])
    printer = PrettyPrinter()
    
    self.assertEqual(printer.to_string(expr), "(v1 AND (false OR v1))")
