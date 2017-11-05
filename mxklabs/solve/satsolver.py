import six

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
  
  def __init__(self, logger):
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

  def __init__(self, logger=lambda msg : print("@CryptoSatSolver: {msg}".format(msg=msg))):
    super(CryptoSatSolver, self).__init__(logger)

  ''' Returns either Solver.RESULT_SAT (if satisfiable), Solver.RESULT_UNSAT (if
      not satisfiable or Solver.RESULT_ERROR on error. If satisfiable, get a satisfying
      assigment (a dictionary mapping from variables to values using get_satisfying_assignment().'''
  def _solve_impl(self):
    
    try:
      import pycryptosat
    except ImportError as e:
      print("error: missing module 'pycryptosat' (see PyPi package 'pycryptosat')")
      exit(1)
    
    # Create a SAT solver.
    pycryptosat_solver = pycryptosat.Solver()
    
    # Move CNF to solver.
    for clause in self.dimacs.clauses:
      pycryptosat_solver.add_clause(clause)
      
    # Get the SAT solver to do our dirty work.
    issat, solution = pycryptosat_solver.solve()

    if issat:
      self.logger("SAT")
      # Make callable satisfying assignment.
      self._satisfying_assignment = lambda lit : bool(solution[lit])      
      return SatSolver.RESULT_SAT
    else:
      self.logger("UNSAT")
      return SatSolver.RESULT_UNSAT

'''
    Implementation of SatSolver using Z3.
'''
class Z3SatSolver(SatSolver):

  def __init__(self, logger=lambda msg : print("@Z3SatSolver: {msg}".format(msg=msg))):
    super(Z3SatSolver, self).__init__(logger)

  ''' Returns either Solver.RESULT_SAT (if satisfiable), Solver.RESULT_UNSAT (if
      not satisfiable or Solver.RESULT_ERROR on error. If satisfiable, get a satisfying
      assigment (a dictionary mapping from variables to values using get_satisfying_assignment().'''
  def _solve_impl(self):

    try:
      import z3
    except ImportError as e:
      print("error: missing module 'z3' (see PyPi package 'z3-solver')")
      exit(1)
    
    z3_vars = [z3.Bool("%d" % v) for v in six.moves.range(self.dimacs.num_vars+1)]
    z3_solver = z3.Solver()
    
    for clause in self.dimacs.clauses:
      z3_clause = []
      
      for lit in clause:
        if lit > 0:
          z3_clause.append(z3_vars[lit])
        else:
          z3_clause.append(z3.Not(z3_vars[lit]))
      
      z3_solver.add(z3.Or(*z3_clause))
      
    z3_result = z3_solver.check()
    
    if z3_result == z3.sat:
      self.logger("SAT")
      # Make callable satisfying assignment.
      model = z3_solver.model()
      self._satisfying_assignment = lambda lit : bool(model[z3_vars[lit]])  
      return SatSolver.RESULT_SAT
    elif z3_result == z3.unsat:
      self.logger("UNSAT")
      return SatSolver.RESULT_UNSAT
    else:    
      self.logger("ERROR")
      return SatSolver.RESULT_ERROR

        