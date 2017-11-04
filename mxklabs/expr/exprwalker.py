''' Walker object. '''

class Visitor(object):
  
  def visit_constant(self, expr, args):
    return self.visit_default(expr, args)
  
  def visit_variable(self, expr, args):
    return self.visit_default(expr, args)
  
  def visit_logical_and(self, expr, args):
    return self.visit_default(expr, args)
  
  def visit_logical_or(self, expr, args):
    return self.visit_default(expr, args)
  
  def visit_logical_not(self, expr, args):
    return self.visit_default(expr, args)
  
  def bottom_up_walk(self, expr):
    return expr.visit(self, dict([(c, self.bottom_up_walk(c)) for c in expr.children()]))
  