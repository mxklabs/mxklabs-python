import itertools
import operator
import six

import pycryptosat as pcs

from mxklabs.expr import expr as ex
from mxklabs.expr import exprtype as et
from mxklabs.expr import expranalyse as ea

from mxklabs.solve import tseitin as st



class Solver(object):
  
  RESULT_SAT = 0
  RESULT_UNSAT = 1
  RESULT_ERROR = 2
  
  def __init__(self, logger=lambda msg : print(msg)):
    self.logger = logger
    self.logger("Solver: '{classname}'".format(classname=self.__class__.__name__))
    
    self.variables = set()
    self.statespace = 0
    
  def _process_constraints(self, constraints):

    # Harvest variables.
    self.variables = set()    
    for constraint in constraints:
      self.variables = self.variables.union(ea.harvest_variables(constraint))
    
    # Work out the number of variable assignments.
    self.statespace = six.moves.reduce(operator.mul, [v.type().num_values() for v in self.variables])

    self.logger("Constaints: {num_constraints}".format(num_constraints=len(constraints)))
    self.logger("Variables: {num_variables}".format(num_variables=len(self.variables)))
    self.logger("State space: {statespace}".format(statespace=self.statespace))

class ExplicitSolver(Solver):

  MAX_STATESPACE = 2 ** 20

  def __init__(self, logger=lambda msg : print(msg)):
    self.satisfying_assignment = None  
    super(ExplicitSolver, self).__init__(logger)

  ''' Returns either Solver.RESULT_SAT (if satisfiable), Solver.RESULT_UNSAT (if
      not satisfiable or Solver.RESULT_ERROR on error. If satisfiable, get a satisfying
      assigment (a dictionary mapping from variables to values using get_satisfying_assignment().'''
  def sat(self, constraints):
    
    # Print some stats.
    self._process_constraints(constraints)
    
    if self.statespace > ExplicitSolver.MAX_STATESPACE:
      self.logger("State space is too large for ExplicitSolver".format(statespace=statespace))
      return Solver.RESULT_ERROR
    else:
      # Get an iterator over all variable assignments.
      variable_assignments = itertools.product(*[v.type().values() for v in variables])
      # Iterate over them.
      for variable_assignment in variable_assignments:
        # For this assignment, create a mapping from variables to values so we can 
        # evaluate the constraints.
        evalargs = {}        
        for v in range(len(variables)):
          variable = variables[v]
          evalargs[variable] = variable_assignment[v]

        if all([constraint.evaluate(evalargs) for constraint in constraints]):
          # All constraints hold under this variable assignment, SAT!
          self.satisfying_assignment = evalargs
          return Solver.RESULT_SAT
        
      # No satisfiable assignment, UNSAT.
      return Solver.RESULT_UNSAT
          
  def get_satisfying_assignment(self):
    return self.satisfying_assignment

class CryptoSatSolver(Solver):

  def __init__(self, logger=lambda msg : print(msg)):
    self.satisfying_assignment = None    
    super(CryptoSatSolver, self).__init__(logger)

  ''' Returns either Solver.RESULT_SAT (if satisfiable), Solver.RESULT_UNSAT (if
      not satisfiable or Solver.RESULT_ERROR on error. If satisfiable, get a satisfying
      assigment (a dictionary mapping from variables to values using get_satisfying_assignment().'''
  def sat(self, constraints):
    
    # Print some stats.
    self._process_constraints(constraints)

    # Create a SAT solver.
    pcs_solver = pcs.Solver()
    
    # Convert expression to CNF.
    tseitin = st.Tseitin()
    tseitin.add_constraints(constraints)
    
    # Move CNF to solver.
    for clause in tseitin.dimacs().clauses:
      pcs_solver.add_clause(clause)
      
    # Get the SAT solver to do our dirty work.
    sat, solution = pcs_solver.solve()

    if sat:
      self.satisfying_assignment = {}
      for variable in self.variables:
        if variable.type() == et.Bool():
          lit = tseitin._lit(variable)
          self.satisfying_assignment[variable] = solution[lit]
        else:
          raise Exception("Only boolean variables are supported")
      
      return Solver.RESULT_SAT
    else:
      return Solver.RESULT_UNSAT
          
  def get_satisfying_assignment(self):
    return self.satisfying_assignment
        