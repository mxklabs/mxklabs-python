import unittest

import mxklabs as mxk

class Test_Expr(unittest.TestCase):

  def test_hashstr(self):    
    self.assertEqual(mxk.LogicalAnd(mxk.Variable(type=mxk.Bool(), id="v1"),mxk.Variable(type=mxk.Bool(), id="v2")).hash_str(), "(logical-and (var v1) (var v2))")
    self.assertEqual(mxk.LogicalAnd(mxk.Variable(type=mxk.Bool(), id="v1"),mxk.Constant(type=mxk.Bool(), value=(True,))).hash_str(), "(logical-and (var v1) (const (true,)))")
    self.assertEqual(mxk.LogicalAnd(mxk.Variable(type=mxk.Bool(), id="v2"),mxk.Variable(type=mxk.Bool(), id="v1")).hash_str(), "(logical-and (var v2) (var v1))")
    self.assertEqual(mxk.LogicalOr(mxk.Constant(type=mxk.Bool(), value=(False,)),mxk.Variable(type=mxk.Bool(), id="v1")).hash_str(), "(logical-or (const (false,)) (var v1))")
    