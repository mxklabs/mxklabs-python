import itertools
import operator
import six

import pycryptosat as pycryptosat

from mxklabs.expr import expr as ex
from mxklabs.expr import exprtype as et
from mxklabs.expr import expranalyse as ea

from mxklabs.solve import tseitin as st
from mxklabs.solve import satsolver as sat

''' 
    Base class for constraint solvers. Constraints solvers can be used to
    decide, given a iterable set of constraints (Expression objects), whether this
    set of constraints is satisfiable. In this context satisfiable means 'there 
    exists an assignment of values to variables under which all constraints 
    evaluate to true'. 
    
    Call solve(constraints). This will return either 
    
    - ConstraintSolver.RESULT_SAT (constraints are satisfiable)
    - ConstraintSolver.RESULT_UNSAT (constraints are not satisfiable)
    - ConstraintSolver.RESULT_ERROR (don't know). 
    
    If solve returns ConstraintSolver.RESULT_SAT then call get_satisfying_assignment 
    for a callable representing a satisfying assignment of values to variables.
'''
class ConstraintSolver(object):

  RESULT_SAT = 0
  RESULT_UNSAT = 1
  RESULT_ERROR = 2
  
  def __init__(self, logger=lambda msg : print(msg)):
    self.logger = logger
    self._satisfying_assignment = None
    self.constraints = None
    self.variables = set()
    self.statespace = 0
    
  def solve(self, constraints):
    # Store constraints.
    self.constraints = constraints
    
    # Harvest variables.
    self.variables = set()    
    for constraint in self.constraints:
      self.variables = self.variables.union(ea.harvest_variables(constraint))
    
    # Work out the number of variable assignments.
    self.statespace = six.moves.reduce(operator.mul, [v.type().num_values() for v in self.variables])

    # Log some stats.
    self.logger("constraint solver: '{classname}'".format(classname=self.__class__.__name__))
    self.logger("num constaints: {num_constraints}".format(num_constraints=len(self.constraints)))
    self.logger("num variables: {num_variables}".format(num_variables=len(self.variables)))
    self.logger("state space: {statespace}".format(statespace=self.statespace))
  
    return self._solve_impl()
  
  ''' 
      To be implemented by derived classes. This function must look at self.constraints and
      decide if this set of constraints is satisfiable. For convenience, self.variable has
      is an iterable collection of all Variable objects in self.constraints. Function must
      return either RESULT_SAT, RESULT_UNSAT or RESULT_ERROR. If satisfiable a callable
      representing a satisfying assignment must be stored in self.satisfying_assignment.
  '''
  def _solve_impl(self):
    raise Exception("don't instantiate ConstraintSolver directly, use a sub-class")
  
  ''' 
      If the last call to solve() returned RESULT_SAT this function returns a callable object
      which maps variables to values, representing the satisfiable assignment.
  '''
  def get_satisfying_assignment(self):
    return self._satisfying_assignment

''' 
    Solver that just enumerates all possible variable assignments and tests form
    satisfiability. 
'''
def BruteForceConstraintSolver(ConstraintSolver):

  # Don't even attempt to brute-force solve problems state spaces exceeding this number.
  MAX_STATESPACE = 2 ** 20

  def __init__(self, logger=lambda msg : print(msg)):
    super(BruteForceConstraintSolver, self).__init__(logger)

  def _solve_impl(self):
    
    if self.statespace <= BruteForceConstraintSolver.MAX_STATESPACE:
      
      # Get an iterator over all variable assignments.
      variable_assignments = itertools.product(*[v.type().values() for v in self.variables])
      # Iterate over them.
      for variable_assignment in variable_assignments:
        # For this assignment, create a mapping from variables to values so we can 
        # evaluate the constraints.
        evalargs = {}        
        for v in range(len(self.variables)):
          variable = self.variables[v]
          evalargs[variable] = variable_assignment[v]

        if all([constraint.evaluate(evalargs) for constraint in self.constraints]):
          # All constraints hold under this variable assignment, SAT!
          self._satisfying_assignment = lambda var : evalargs[var]
          return ConstraintSolver.RESULT_SAT
        
      # No satisfiable assignment, UNSAT.
      return ConstraintSolver.RESULT_UNSAT
    
    else:

      # We're not patient enough to solve this problem using brute force.
      self.logger("state space is too large for '{classname}'".format(classname=self.__class__.__name__))
      return Solver.RESULT_ERROR

''' 
    Solver that converts constraints to a boolean CNF using a Tseitin-like
    conversion and then establishes satisfiability using a SAT solver.
'''
class TseitinConstraintSolver(ConstraintSolver):
  
  def __init__(self, sat_solver_type=sat.CryptoSatSolver, logger=lambda msg : print(msg)):
    self.sat_solver_type = sat_solver_type
    super(TseitinConstraintSolver, self).__init__(logger)
  
  def _solve_impl(self):
    
    # Convert constraints to CNF using a Tseitin conversion.
    tseitin = st.Tseitin()
    tseitin.add_constraints(self.constraints)
    
    # Make a SAT solver.
    sat_solver = self.sat_solver_type()
    
    # Solve CNF using our SAT solver.
    sat_result = sat_solver.solve(tseitin.dimacs())
    
    # Convert the result.
    if sat_result == sat.SatSolver.RESULT_SAT:
      
      def sat_ass(variable):
        if variable.type() == et.Bool():
          lit = tseitin._lit(variable)
          return bool(sat_solver.get_satisfying_assignment()(lit))
        else:
          raise Exception("Only boolean variables are supported")
        
      self._satisfying_assignment = sat_ass
      return ConstraintSolver.RESULT_SAT
    elif sat_result == sat.SatSolver.RESULT_SAT:
      return ConstraintSolver.RESULT_UNSAT
    else:
      return ConstraintSolver.RESULT_ERROR
    
