import six

import pycryptosat

from mxklabs.expr import expr as ex

''' 
    Base class for SAT solvers. SAT solvers can be used to decide if a boolean 
    formula in CNF form is satisfiable. In this context satisfiable means 'there 
    exists an assignment of values to boolean variables under which all clauses 
    evaluate to true'. 
    
    Call solve(dimacs) where dimacs is a mxklabs.Dimacs object. This call will return either 
    
    - SatSolver.RESULT_SAT (dimacs is satisfiable)
    - SatSolver.RESULT_UNSAT (dimacs is not satisfiable)
    - SatSolver.RESULT_ERROR (don't know). 
    
    If solve returns SatSolver.RESULT_SAT then call get_satisfying_assignment 
    for a callable representing a satisfying assignment of values to variables.
    Variables in this context are integers and values are True or False.
'''
class SatSolver(object):
  
  RESULT_SAT = 0
  RESULT_UNSAT = 1
  RESULT_ERROR = 2
  
  def __init__(self, logger=lambda msg : print(msg)):
    self.logger = logger
    self.dimacs = None
    self.statespace = None
    self.variables = None
    self._satisfying_assignment = None
    
  def solve(self, dimacs):

    # Store.
    self.dimacs = dimacs
    self.variables = six.moves.range(1, dimacs.num_vars+1)
    
    # Work out the number of variable assignments.
    self.statespace = 2 ** dimacs.num_vars

    # Log some stats.
    self.logger("sat solver: '{classname}'".format(classname=self.__class__.__name__))
    self.logger("num variables: {num_variables}".format(num_variables=dimacs.num_vars))
    self.logger("num clauses: {num_clauses}".format(num_clauses=len(dimacs.clauses)))
    self.logger("state space: {statespace}".format(statespace=self.statespace))
    
    # Solve.
    return self._solve_impl()

  ''' 
      To be implemented by derived classes. This function must look at self.constraints and
      decide if this set of constraints is satisfiable. For convenience, self.variable has
      is an iterable collection of all Variable objects in self.constraints. Function must
      return either RESULT_SAT, RESULT_UNSAT or RESULT_ERROR. If satisfiable a callable
      representing a satisfying assignment must be stored in self.satisfying_assignment.
  '''
  def _solve_impl(self):
    raise Exception("don't instantiate SatSolver directly, use a sub-class")
  
  ''' 
      If the last call to solve() returned RESULT_SAT this function returns a callable object
      which maps variables to values, representing the satisfiable assignment.
  '''
  def get_satisfying_assignment(self):
    return self._satisfying_assignment

''' 
    Implementation of SatSolver using cryptosat. 
'''
class CryptoSatSolver(SatSolver):

  def __init__(self, logger=lambda msg : print(msg)):
    super(CryptoSatSolver, self).__init__(logger)

  ''' Returns either Solver.RESULT_SAT (if satisfiable), Solver.RESULT_UNSAT (if
      not satisfiable or Solver.RESULT_ERROR on error. If satisfiable, get a satisfying
      assigment (a dictionary mapping from variables to values using get_satisfying_assignment().'''
  def _solve_impl(self):
    
    # Create a SAT solver.
    pycryptosat_solver = pycryptosat.Solver()
    
    # Move CNF to solver.
    for clause in self.dimacs.clauses:
      pycryptosat_solver.add_clause(clause)
      
    # Get the SAT solver to do our dirty work.
    issat, solution = pycryptosat_solver.solve()

    if issat:     
      # Make callable satisfying assignment.
      self._satisfying_assignment = lambda lit : bool(solution[lit])      
      return SatSolver.RESULT_SAT
    else:
      return SatSolver.RESULT_UNSAT
        