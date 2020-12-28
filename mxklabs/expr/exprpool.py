class ExprPool:

  def __init__(self):
    self.pool = {}

  def make_unique(self, expr):
    if expr in self.pool:
      return self.pool[expr]
    else:
      self.pool[expr] = expr
      return expr

