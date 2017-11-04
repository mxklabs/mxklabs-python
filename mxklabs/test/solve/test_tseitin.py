import unittest

import mxklabs as mxk

class Test_Tseitin(unittest.TestCase):
    
  def test_tseitin_true(self):
    true_ = mxk.Constant(type=mxk.Bool(), value=True)
    
    tseitin = mxk.Tseitin()

    tseitin.add_constraint(true_)
    
    self.assertEqual([[1]], tseitin.dimacs().clauses)
    
    