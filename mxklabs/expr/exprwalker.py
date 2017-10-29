''' Walker object. '''

class Visitor(object):
  
  def bottom_up_walk(self, expr):
    return expr.visit(self, dict([(c, self.bottom_up_walk(c)) for c in expr.children()]))