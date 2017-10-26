import unittest

import mxklabs.expr as e

class Test_Expr(unittest.TestCase):
  
  def test_Bool(self):   
    T = e.Bool
    self.assertEqual("bool", str(T))
    self.assertEqual([False, True], [value for value in T.values()])
    self.assertEqual(2, T.num_values())
    
  def test_BitVector(self):    
    T = e.BitVector(3)
    self.assertEqual("uint3", str(T))
    self.assertEqual([0,1,2,3,4,5,6,7], [value for value in T.values()])
    self.assertEqual(8, T.num_values())
    
  def test_Product(self):    
    T = e.Product([e.BitVector(2),e.Bool])
    self.assertEqual("(uint2,bool)", str(T))
    self.assertEqual([(0, False), (0, True), (1, False), (1, True), (2, False), (2, True), (3, False), (3, True)], [value for value in T.values()])
    self.assertEqual(8, T.num_values())
  
  def test_expr_hashstr(self):    
    self.assertEqual(e.And([e.Var(e.Bool, "v1"),e.Var(e.Bool, "v2")])._hashstr, "(and (var v1) (var v2))")
    self.assertEqual(e.And([e.Var(e.Bool, "v1"),e.Const(e.Bool, True)])._hashstr, "(and (var v1) (const true))")
    self.assertEqual(e.And([e.Var(e.Bool, "v2"),e.Var(e.Bool, "v1")])._hashstr, "(and (var v2) (var v1))")
    self.assertEqual(e.Or([e.Const(e.Bool, False),e.Var(e.Bool, "v1")])._hashstr, "(or (const false) (var v1))")
    
  def test_expr_walker(self):
    
    class PrettyPrinter(e.Visitor):
      def to_string(self, expr): return self.bottom_up_walk(expr);
      
      def visit_var(self, expr, args): return str(expr.id)
      def visit_const(self, expr, args): return str(expr.value).lower()
      def visit_and(self, expr, args): return "(" + " AND ".join([args[c] for c in expr.children()]) + ")"
      def visit_or(self, expr, args): return "(" + " OR ".join([args[c] for c in expr.children()]) + ")"
      def visit_not(self, expr, args): return "(NOT" + args[expr.children()[0]] + ")"
    
    expr = e.And([e.Var(e.Bool, "v1"),e.Or([e.Const(e.Bool, False),e.Var(e.Bool, "v1")])])
    printer = PrettyPrinter()
    
    self.assertEqual(printer.to_string(expr), "(v1 AND (false OR v1))")
