import unittest

import mxklabs as mxk

class Test_SatSolver(unittest.TestCase):
  
  def test_sat_solver_sat(self):
    
    for sat_solver_type in mxk.Utils.get_derived_classes(mxk, mxk.SatSolver):

      dimacs_string = "c  simple_v3_c2.cnf\n" + \
                      "p cnf 3 2\n" + \
                      "-1 -3 0\n" + \
                      "1 0\n" 
                    
      dimacs = mxk.DimacsParser(string=dimacs_string)

      solver = sat_solver_type(logger=lambda msg : None)
    
      self.assertEqual(mxk.SatSolver.RESULT_SAT, solver.solve(dimacs))
      self.assertTrue(solver.get_satisfying_assignment()(1))
      self.assertFalse(solver.get_satisfying_assignment()(3))
  
  def test_sat_solver_unsat(self):
    
    for sat_solver_type in mxk.Utils.get_derived_classes(mxk, mxk.SatSolver):

      dimacs_string = "c  simple_v3_c2.cnf\n" + \
                      "p cnf 3 3\n" + \
                      "-1 -3 0\n" + \
                      "1 0\n" + \
                      "3 0\n" 
                    
      dimacs = mxk.DimacsParser(string=dimacs_string)

      solver = sat_solver_type(logger=lambda msg : None)
    
      self.assertEqual(mxk.SatSolver.RESULT_UNSAT, solver.solve(dimacs))
          