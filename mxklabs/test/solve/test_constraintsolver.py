import unittest

import mxklabs as mxk

class Test_Solver(unittest.TestCase):
  
  def test_sat(self):

    x_ = mxk.Variable(type=mxk.Bool(), id='x')  
    y_ = mxk.Variable(type=mxk.Bool(), id='y')
    
    x_or_y_ = mxk.LogicalOr(x_, y_)
    not_x_ = mxk.LogicalNot(x_)

    solver = mxk.TseitinConstraintSolver()
   
    self.assertEqual(mxk.ConstraintSolver.RESULT_SAT, solver.solve([x_or_y_, not_x_]))
    
    self.assertFalse(solver.get_satisfying_assignment()(x_))
    self.assertTrue(solver.get_satisfying_assignment()(y_))
    