import itertools
import operator
import six

import mxklabs.expr as e

class Solver(object):

  def __init__(self, logger=lambda msg : print(msg)):
    self.logger = logger

  def solve(self, constraints):
    variables = set()
    
    for constraint in constraints:
      variables = variables.union(e.harvest_variables(constraint))

    variables = list(variables)

    self.logger("Constaints: {num_constraints}".format(num_constraints=len(constraints)))
    self.logger("Variables: {num_variables}".format(num_variables=len(variables)))
    
    statespace = six.moves.reduce(operator.mul, [v.type().num_values() for v in variables])
    
    self.logger("State space: {statespace}".format(statespace=statespace))
    
    variable_assignments = itertools.product(*[v.type().values() for v in variables])
    
    for variable_assignment in variable_assignments:
      
      evalargs = {}
      
      for v in range(len(variables)):
        variable = variables[v]
        evalargs[variable] = variable_assignment[v]

      if all([constraint.evaluate(evalargs) for constraint in constraints]):
        print("SAT (" + str(evalargs) + ")")
        return True
    
    print("UNSAT")
    return False