import unittest

import mxklabs.expr as e

class Test_Expr(unittest.TestCase):

  def test_hashstr(self):    
    self.assertEqual(e.LogicalAnd(e.Variable(type=e.Bool(), id="v1"),e.Variable(type=e.Bool(), id="v2"))._hashstr, "(logical-and (var v1) (var v2))")
    self.assertEqual(e.LogicalAnd(e.Variable(type=e.Bool(), id="v1"),e.Constant(type=e.Bool(), value=True))._hashstr, "(logical-and (var v1) (const true))")
    self.assertEqual(e.LogicalAnd(e.Variable(type=e.Bool(), id="v2"),e.Variable(type=e.Bool(), id="v1"))._hashstr, "(logical-and (var v2) (var v1))")
    self.assertEqual(e.LogicalOr(e.Constant(type=e.Bool(), value=False),e.Variable(type=e.Bool(), id="v1"))._hashstr, "(logical-or (const false) (var v1))")
    