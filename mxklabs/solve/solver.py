class Solver(object):

  def __init__(self, logger=lambda msg : print(msg)):
    self.logger = logger

  def solve(self, constraints):
    self.logger("Constaints: {num_constraints}".format(num_constraints=len(constraints)))
  
