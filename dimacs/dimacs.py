class Dimacs(object):
  def __init__(self, num_vars=None, num_clauses=None, clauses=None):
    self.num_vars = num_vars
    self.num_clauses = num_clauses
    self.clauses = clauses
