import unittest

import mxklabs as mxk

class Test_ConstraintSolver(unittest.TestCase):
  
  def test_constraintsolver_sat(self):
    
    for constraint_solver_type in mxk.Utils.get_derived_classes(mxk, mxk.ConstraintSolver):

      x_ = mxk.Variable(type='bool', id='x')  
      y_ = mxk.Variable(type='bool', id='y')
      
      x_or_y_ = mxk.LogicalOr(x_, y_)
      not_x_ = mxk.LogicalNot(x_)

      solver = constraint_solver_type(logger=lambda msg : None)
    
      self.assertEqual(mxk.ConstraintSolver.RESULT_SAT, solver.solve([x_or_y_, not_x_]))
      
      self.assertFalse(solver.get_satisfying_assignment()(x_))
      self.assertTrue(solver.get_satisfying_assignment()(y_))
    
  def test_constraintsolver_unsat(self):
    
    for constraint_solver_type in mxk.Utils.get_derived_classes(mxk, mxk.ConstraintSolver):

      x_ = mxk.Variable(type='bool', id='x')  
      y_ = mxk.Variable(type='bool', id='y')
      
      x_or_y_ = mxk.LogicalOr(x_, y_)
      not_x_ = mxk.LogicalNot(x_)
      not_y_ = mxk.LogicalNot(y_)

      solver = constraint_solver_type(logger=lambda msg : None)
    
      self.assertEqual(mxk.ConstraintSolver.RESULT_UNSAT, solver.solve([x_or_y_, not_x_, not_y_]))
      